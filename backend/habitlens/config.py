from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
PARENT_PAGE_ID = os.getenv("PARENT_PAGE_ID")
MOCK_HABITS_PATH = os.getenv("MOCK_HABITS_PATH")
HABITS_PATH = os.getenv("HABITS_PATH")


def get_chat_model(model_name: str = "openai:gpt-5"):
    """Returns a LangChain chat model initialized with the API key from the environment."""
    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise EnvironmentError("API_KEY environment variable not set.")

    return init_chat_model(model=model_name, api_key=api_key)
