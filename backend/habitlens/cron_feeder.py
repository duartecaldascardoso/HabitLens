from notion_client import Client

from backend.habitlens.config import NOTION_TOKEN, PARENT_PAGE_ID

notion = Client(auth=NOTION_TOKEN)

def get_or_create_weekly_subpage(parent_id, title):
    """Search or create a subpage under the annual report page."""
    children = notion.blocks.children.list(parent_id)["results"]
    for block in children:
        if block["type"] == "child_page" and block["child_page"]["title"] == title:
            return block["id"]

    # Create the weekly subpage
    new_page = notion.pages.create(
        parent={"page_id": parent_id},
        properties={"title": [{"type": "text", "text": {"content": title}}]},
        children=[
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": title}}]}
            }
        ]
    )
    return new_page["id"]

def add_text_block(page_id, text):
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}
            }
        ]
    )

def add_image_block(page_id, image_url):
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {"url": image_url}
                }
            }
        ]
    )

# === Main logic ===
def update_ai_reports(start_date, end_date, summary_text, image_url):
    """
    - Create or update weekly report as a subpage
    - Append summary to the 2025 Annual Report
    """
    week_title = f"Weekly Report – {start_date} to {end_date}"

    # Create subpage under the annual report page
    weekly_page_id = get_or_create_weekly_subpage(PARENT_PAGE_ID, week_title)

    # Add detailed content to the weekly subpage
    add_text_block(weekly_page_id, summary_text)
    add_image_block(weekly_page_id, image_url)

    # Append a one-line summary to the annual report parent page
    one_liner = summary_text.splitlines()[0]  # First line only
    add_text_block(PARENT_PAGE_ID, f"{start_date} to {end_date}: {one_liner}")

if __name__ == "__main__":
    # Demo run
    start = "2025-07-08"
    end = "2025-07-14"
    summary = """Mood was mostly positive. Sleep average: 7.1h. 
Top habits: Reading, Gym, Music. 
Energy level was high on 4 of 7 days."""
    image_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Graph_example.svg/500px-Graph_example.svg.png"

    update_ai_reports(start, end, summary, image_link)
