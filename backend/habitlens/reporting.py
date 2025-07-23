from notion_client import Client
from backend.habitlens.config import NOTION_TOKEN, PARENT_PAGE_ID

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


def add_image_block(page_id: str, image_url: str):
    """Add an image block from an external URL to a Notion page."""
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {"url": image_url},
                },
            }
        ],
    )


def write_weekly_report_to_notion(
    start_date: str,
    end_date: str,
    summary_text: str,
    image_urls: list[str] = None,
):
    """
    Create a weekly report page under the parent page and write a summary with optional images.
    """
    week_title = f"Weekly Report – {start_date} to {end_date}"
    page_id = get_or_create_weekly_subpage(PARENT_PAGE_ID, week_title)

    add_text_block(page_id, summary_text)

    if image_urls:
        for url in image_urls:
            add_image_block(page_id, url)
