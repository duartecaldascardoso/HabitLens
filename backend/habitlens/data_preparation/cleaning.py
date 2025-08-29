import pandas as pd

from backend.habitlens.data_preparation.habit_feature_engineering import (
    HabitFeatureEngineer,
)


def _clean_habit_features(df: pd.DataFrame) -> pd.DataFrame:
    """Runs the feature engineering process to clear null values and categorical data."""
    feature_engineering = HabitFeatureEngineer()
    cleaned_features_df = feature_engineering.transform(df)

    return cleaned_features_df


def get_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the cleaned DataFrame."""

    cleaned_features_df = _clean_habit_features(df)

    # Converting Date into a datetime object
    cleaned_features_df["Date"] = pd.to_datetime(cleaned_features_df["Date"])

    # Add more steps here if more cleaning/feature engineering is needed. Good for now
    return cleaned_features_df
