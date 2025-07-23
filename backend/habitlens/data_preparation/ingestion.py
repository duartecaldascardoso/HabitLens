import os
from pathlib import Path
from typing import List

import pandas as pd
from notion_client import Client

from backend.habitlens.config import NOTION_TOKEN, DATABASE_ID
from backend.habitlens.utils import extract_property_value

notion = Client(auth=NOTION_TOKEN)


def _fetch_all_pages() -> List:
    """Uses the notion client to get the database by ID and return the information."""
    results = []
    start_cursor = None

    while True:
        response = notion.databases.query(
            **{
                "database_id": DATABASE_ID,
                "start_cursor": start_cursor,
            }
            if start_cursor
            else {
                "database_id": DATABASE_ID,
            }
        )

        results.extend(response["results"])
        if not response.get("has_more"):
            break
        start_cursor = response.get("next_cursor")

    return results


def _parse_pages(pages) -> List[dict]:
    """Parse raw Notion pages into a list of dynamic structured dicts."""
    data = []

    for page in pages:
        props = page["properties"]
        row = {}

        for name, prop in props.items():
            row[name] = extract_property_value(prop)

        data.append(row)

    return data


def _get_daily_habits() -> List[dict]:
    """Entry point to fetch and parse daily habit entries."""
    pages = _fetch_all_pages()
    structured_data = _parse_pages(pages)
    return structured_data


def fetch_information_from_notion_into_csv(user_identifier: str = "") -> str:
    """Isolated scrip caller to ingest all the information from Notion and export it to a CSV file."""
    dataframe = pd.DataFrame(_get_daily_habits())
    csv_path = f"backend/habitlens/data/habits{user_identifier}.csv"

    Path(os.path.dirname(csv_path)).mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(csv_path, index=False)
    print(f"Exported to {csv_path}")

    return csv_path
