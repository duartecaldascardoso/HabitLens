import asyncio
import os
import csv
from pathlib import Path
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.constants import END
from langgraph.graph import StateGraph, START

from backend.habitlens.weekly_graph.schemas.sorting_algorithm import WeeklyOverview
from backend.habitlens.weekly_graph.prompt import WEEKLY_OVERVIEW_PROMPT
from backend.habitlens.weekly_graph.state import InputWeeklyOverviewState, WeeklyOverviewState

load_dotenv()

"""This graph will be executed once a week and will directly write to the Notion page from the user."""

async def _load_and_parse_csv(state: InputWeeklyOverviewState):
    """Load and parse the weekly data CSV."""
    csv_path = Path(state.csv_path)
    week_data = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            week_data.append(dict(row))
    return {"week_data": week_data}

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

async def _output_overview(state: WeeklyOverviewState):
    """Output or save the weekly overview."""
    print("\n--- Weekly Overview ---")
    print(state.weekly_overview)
    return {"output_success": True}

# Build the graph
builder = StateGraph(WeeklyOverviewState)
builder.add_node("load_and_parse_csv", _load_and_parse_csv)
builder.add_node("generate_weekly_overview", _generate_weekly_overview)
builder.add_node("output_overview", _output_overview)

builder.add_edge(START, "load_and_parse_csv")
builder.add_edge("load_and_parse_csv", "generate_weekly_overview")
builder.add_edge("generate_weekly_overview", "output_overview")
builder.add_edge("output_overview", END)

graph = builder.compile()

async def main():
    initial_state = WeeklyOverviewState(
        csv_path="path/to/your/weekly_data.csv",
        user_identifier="mock_user"
    )
    result = await graph.ainvoke(initial_state)
    if result.get("output_success"):
        print("Weekly overview generated and output successfully.")

if __name__ == "__main__":
    asyncio.run(main())