from typing import List

from notion_client import Client

from backend.habitlens.config import NOTION_TOKEN, DATABASE_ID
from backend.habitlens.utils import extract_property_value

notion = Client(auth=NOTION_TOKEN)


def fetch_all_pages() -> List:
    """Uses the notion client to get the database by ID and return the information."""
    results = []
    start_cursor = None

    while True:
        response = notion.databases.query(
            **{
                "database_id": DATABASE_ID,
                "start_cursor": start_cursor,
            } if start_cursor else {
                "database_id": DATABASE_ID,
            }
        )

        results.extend(response["results"])
        if not response.get("has_more"):
            break
        start_cursor = response.get("next_cursor")

    return results


def parse_pages(pages) -> List[dict]:
    """Parse raw Notion pages into a list of dynamic structured dicts."""
    data = []

    for page in pages:
        props = page["properties"]
        row = {}

        for name, prop in props.items():
            row[name] = extract_property_value(prop)

        data.append(row)

    return data


def get_daily_habits() -> List[dict]:
    """Entry point to fetch and parse daily habit entries."""
    pages = fetch_all_pages()
    structured_data = parse_pages(pages)
    return structured_data
