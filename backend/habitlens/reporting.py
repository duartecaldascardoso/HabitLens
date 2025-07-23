from notion_client import Client
from backend.habitlens.config import NOTION_TOKEN, PARENT_PAGE_ID
from backend.habitlens.utils import split_text_into_chunks
from backend.habitlens.weekly_graph.schemas.weekly_overview import WeeklyOverview

notion = Client(auth=NOTION_TOKEN)


def get_or_create_weekly_subpage(parent_id: str, title: str) -> str:
    """Search or create a subpage with the given title under the parent Notion page."""
    children = notion.blocks.children.list(parent_id)["results"]
    for block in children:
        if block["type"] == "child_page" and block["child_page"]["title"] == title:
            return block["id"]

    # Create a new subpage
    new_page = notion.pages.create(
        parent={"page_id": parent_id},
        properties={"title": [{"type": "text", "text": {"content": title}}]},
    )
    return new_page["id"]


def add_text_block_with_title(page_id: str, title: str, text: str):
    """Add a text block with a title to a Notion page, handling text chunking."""
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": title}}]
                },
            }
        ],
    )

    text_chunks = split_text_into_chunks(text, 1900)
    for chunk in text_chunks:
        add_text_block(page_id, chunk)


def add_text_block(page_id: str, text: str):
    """Add a paragraph text block to a Notion page."""
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                },
            }
        ],
    )


def write_weekly_overview_to_notion(page_id: str, weekly_overview: WeeklyOverview):
    """Write the weekly overview to a Notion page with consistent section formatting."""

    add_text_block_with_title(page_id, "📊 Weekly Summary", weekly_overview.weekly_summary)
    add_text_block_with_title(page_id, "🔍 Key Observations", weekly_overview.key_observations)
    add_text_block_with_title(page_id, "🌱 Areas for Improvement", weekly_overview.improvement_areas)
    add_text_block_with_title(page_id, "💡 Recommended Habits", weekly_overview.habit_recommendations)
