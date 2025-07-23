import asyncio
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.constants import END
from langgraph.graph import StateGraph, START

from backend.habitlens.data_preparation.ingestion import (
    fetch_information_from_notion_into_csv,
)
from backend.habitlens.utils import obtain_dataframe_from_path
from backend.habitlens.weekly_graph.schemas.sorting_algorithm import WeeklyOverview
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


async def _ingest_notion_data(state: InputWeeklyOverviewState):
    """Used to ingest the data from Notion and obtain the last two weeks of data."""

    # This makes sure that the .csv file from the user is up to date.
    csv_path = fetch_information_from_notion_into_csv(
        user_identifier=state.user_identifier
    )

    return {"csv_path": csv_path}


async def _clean_and_extract_data(state: WeeklyOverviewState):
    """Used to get the clean data from the last two weeks."""

    clean_df = obtain_dataframe_from_path(csv_path=state.csv_path)


async def _generate_weekly_overview(state: WeeklyOverviewState):
    """Generate a weekly overview using an LLM."""
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise EnvironmentError("API_KEY environment variable not set.")
    model = init_chat_model(model="gpt-4o-mini", api_key=api_key)
    prompt = WEEKLY_OVERVIEW_PROMPT + f"\nData: {state.week_data}"
    response = await model.with_structured_output(WeeklyOverview).ainvoke(
        [HumanMessage(content=prompt)]
    )
    return {"weekly_overview": response}


# Build the graph
builder = StateGraph(WeeklyOverviewState)
builder.add_node("ingest_notion_data", _ingest_notion_data)
builder.add_node("clean_and_extract_data", _clean_and_extract_data)
builder.add_node("generate_weekly_overview", _generate_weekly_overview)

builder.add_edge(START, "ingest_notion_data")
builder.add_edge("ingest_notion_data", "clean_and_extract_data")
builder.add_edge("clean_and_extract_data", "generate_weekly_overview")
builder.add_edge("generate_weekly_overview", END)

graph = builder.compile()


async def main():
    initial_state = InputWeeklyOverviewState(user_identifier="")
    result = await graph.ainvoke(initial_state)
    if result.get("output_success"):
        print("Weekly overview generated and output successfully.")


if __name__ == "__main__":
    asyncio.run(main())
