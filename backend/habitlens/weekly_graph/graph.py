import asyncio
from datetime import datetime, timedelta

from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langgraph.constants import END
from langgraph.graph import StateGraph, START

from backend.habitlens.config import get_chat_model, PARENT_PAGE_ID
from backend.habitlens.data_preparation.ingestion import (
    fetch_information_from_notion_into_csv,
)
from backend.habitlens.reporting import (
    get_or_create_weekly_subpage,
    write_weekly_overview_to_notion,
)
from backend.habitlens.utils import obtain_dataframe_from_path
from backend.habitlens.weekly_graph.schemas.weekly_overview import WeeklyOverview
from backend.habitlens.weekly_graph.prompt import WEEKLY_OVERVIEW_PROMPT
from backend.habitlens.weekly_graph.state import (
    InputWeeklyOverviewState,
    WeeklyOverviewState,
)

load_dotenv()

"""This graph will be executed once a week and will directly write to the Notion page from the user."""


# Step order:
# 1. Ingest information from Notion
# 2. Clean the information and extract information from the last two weeks
# 3. Generate a weekly overview using an LLM
# 4. Write the generated weekly overview to the Notion page


async def _ingest_notion_data(state: InputWeeklyOverviewState):
    """Used to ingest the data from Notion and get the last two weeks of data."""

    # This makes sure that the .csv file from the user is up to date.
    csv_path = fetch_information_from_notion_into_csv(
        user_identifier=state.user_identifier
    )

    return {"csv_path": csv_path}


async def _clean_and_extract_data(state: WeeklyOverviewState):
    """Used to get the clean data from the last two weeks."""

    clean_df = obtain_dataframe_from_path(csv_path=state.csv_path)

    # Collecting the data from the last two weeks
    two_weeks_ago = datetime.today() - timedelta(days=14)
    last_two_weeks_df = clean_df[clean_df["Date"] >= two_weeks_ago]

    return {"week_data": last_two_weeks_df.to_dict(orient="records")}


async def _generate_weekly_overview(state: WeeklyOverviewState):
    """Generate a weekly overview using an LLM."""
    model = get_chat_model()
    prompt = WEEKLY_OVERVIEW_PROMPT.format(user_data=state.week_data)
    response = await model.with_structured_output(WeeklyOverview).ainvoke(
        [HumanMessage(content=prompt)]
    )
    return {"weekly_overview": response}


async def _write_to_notion(state: WeeklyOverviewState):
    """Write the generated weekly overview to Notion with structured formatting."""
    weekly_overview = state.weekly_overview

    today = datetime.today().date()
    start_date = today - timedelta(days=7)
    end_date = today

    # Get the page ID for the weekly report
    week_title = f"Weekly Report – {start_date} to {end_date}"
    page_id = get_or_create_weekly_subpage(PARENT_PAGE_ID, week_title)

    # Pass the required parameters to the function
    write_weekly_overview_to_notion(page_id=page_id, weekly_overview=weekly_overview)

    return {"output_success": True}


# Build the graph
builder = StateGraph(WeeklyOverviewState)
builder.add_node("ingest_notion_data", _ingest_notion_data)
builder.add_node("clean_and_extract_data", _clean_and_extract_data)
builder.add_node("generate_weekly_overview", _generate_weekly_overview)
builder.add_node("write_to_notion", _write_to_notion)

builder.add_edge(START, "ingest_notion_data")
builder.add_edge("ingest_notion_data", "clean_and_extract_data")
builder.add_edge("clean_and_extract_data", "generate_weekly_overview")
builder.add_edge("generate_weekly_overview", "write_to_notion")
builder.add_edge("write_to_notion", END)

graph = builder.compile()


async def main():
    initial_state = InputWeeklyOverviewState(user_identifier="")
    result = await graph.ainvoke(initial_state)
    if result.get("output_success"):
        print("Weekly overview generated and output successfully.")


if __name__ == "__main__":
    asyncio.run(main())
