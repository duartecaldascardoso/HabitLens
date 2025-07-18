from dotenv import load_dotenv
import os

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
PARENT_PAGE_ID = os.getenv("PARENT_PAGE_ID")
