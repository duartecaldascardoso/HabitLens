"""Helper functions for HabitLens."""

import pandas as pd

from backend.habitlens.config import MOCK_HABITS_PATH, HABITS_PATH
from backend.habitlens.data_preparation.cleaning import get_clean_dataframe


def extract_property_value(prop):
    """Helper to safely extract a Notion property value. Properties can be of various types and unsafe to access directly."""
    if prop is None:
        return None

    if "checkbox" in prop:
        return prop["checkbox"]
    if "select" in prop and prop["select"]:
        return prop["select"]["name"]
    if "multi_select" in prop and prop["multi_select"]:
        return [tag["name"] for tag in prop["multi_select"]]
    if "number" in prop:
        return prop["number"]
    if "date" in prop and prop["date"]:
        return prop["date"]["start"]
    if "rich_text" in prop and prop["rich_text"]:
        return prop["rich_text"][0]["plain_text"]

    return None


def load_mock_data() -> pd.DataFrame:
    """Load mock data from the specified path."""
    try:
        df = pd.read_csv(MOCK_HABITS_PATH)
        return df
    except FileNotFoundError:
        print(f"Mock data file not found at {MOCK_HABITS_PATH}. Please check the path.")
        return pd.DataFrame()


def load_habit_data() -> pd.DataFrame:
    """Load habit data from the specified path."""
    try:
        df = pd.read_csv(HABITS_PATH)
        return df
    except FileNotFoundError:
        print(f"Habit data file not found at {HABITS_PATH}. Please check the path.")
        return pd.DataFrame()


def obtain_clean_dataframe() -> pd.DataFrame:
    """Returns the cleaned DataFrame."""

    df = load_habit_data()
    if df.empty:
        print("Habit data is empty. Please check the data source.")
        return pd.DataFrame()
    return get_clean_dataframe(df)


def obtain_mock_dataframe() -> pd.DataFrame:
    """Returns the mock DataFrame."""

    df = load_mock_data()
    if df.empty:
        print("Mock data is empty. Please check the data source.")
        return pd.DataFrame()
    return get_clean_dataframe(df)


def obtain_dataframe_from_path(csv_path: str) -> pd.DataFrame:
    """Returns a DataFrame from the specified CSV path."""
    try:
        df = pd.read_csv(csv_path)
        return get_clean_dataframe(df)
    except FileNotFoundError:
        print(f"CSV file not found at {csv_path}. Please check the path.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print(f"CSV file at {csv_path} is empty.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return pd.DataFrame()


def split_text_into_chunks(text, max_length=1900):
    """Split text into chunks of specified maximum length, trying to break at paragraph boundaries."""
    if not text or len(text) <= max_length:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current_chunk = ""

    for paragraph in paragraphs:
        # If adding this paragraph exceeds the limit, store the current chunk and start a new one
        if len(current_chunk) + len(paragraph) + 2 > max_length:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = paragraph
            else:
                # Handle a case where a single paragraph is longer than max_length
                para_chunks = [
                    paragraph[i : i + max_length]
                    for i in range(0, len(paragraph), max_length)
                ]
                chunks.extend(para_chunks[:-1])
                current_chunk = para_chunks[-1]
        else:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
