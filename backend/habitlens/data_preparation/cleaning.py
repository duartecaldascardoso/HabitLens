import pandas as pd

from backend.habitlens.config import HABITS_PATH, MOCK_HABITS_PATH
from backend.habitlens.data_preparation.habit_feature_engineering import (
    HabitFeatureEngineer,
)

data_source = [HABITS_PATH, MOCK_HABITS_PATH]
dataframe = pd.read_csv(data_source[1])


def _clean_habit_features(df: pd.DataFrame) -> pd.DataFrame:
    """Runs the feature engineering process to clear null values and categorical data."""
    feature_engineering = HabitFeatureEngineer()
    cleaned_features_df = feature_engineering.transform(df)

    return cleaned_features_df


def get_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the cleaned DataFrame."""

    cleaned_features_df = _clean_habit_features(df)

    # Add more steps here if more cleaning/feature engineering is needed. Good for now
    return cleaned_features_df