"""Helper functions for HabitLens."""
import pandas as pd

from backend.habitlens.config import MOCK_HABITS_PATH, HABITS_PATH
from backend.habitlens.data_preparation.cleaning import get_clean_dataframe

data_source = [HABITS_PATH, MOCK_HABITS_PATH]
dataframe = pd.read_csv(data_source[1])

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

def obtain_clean_dataframe() ->pd.DataFrame:
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