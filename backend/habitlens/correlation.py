from typing import List

import pandas as pd
import ast
from sklearn.preprocessing import MultiLabelBinarizer

df = pd.read_csv("data/mock_habits.csv")


def _prepare_correlation_data() -> pd.DataFrame:
    """Clean the DataFrame by removing unnecessary columns and converting data types."""

    # Mappers for converting categorical data to numerical scores
    mood_map = {
        "Terrible": 1,
        "Sad": 2,
        "Meh": 3,
        "Neutral": 4,
        "Good": 5,
        "Great": 6,
        "Amazing": 7,
    }
    energy_map = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}

    df["Mood_score"] = df["Mood"].map(mood_map)
    df["Energy_score"] = df["Energy Level"].map(energy_map)
    df["Reading"] = df["Reading"].astype(int)

    correlation_df = df[["Mood_score", "Energy_score", "Sleep Hours", "Reading"]]

    df["Gym"] = df["Gym"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )
    mlb = MultiLabelBinarizer()
    gym_encoded = pd.DataFrame(
        mlb.fit_transform(df["Gym"]), columns=[f"Gym: {g}" for g in mlb.classes_]
    )
    correlation_df = pd.concat([correlation_df, gym_encoded], axis=1)

    return correlation_df


def _phrased_correlation_data(correlation_df: pd.DataFrame, target_attribute: str) -> List[str]:
    """Generate phrases based on the correlation data for a specific attribute."""
    phrases = []
    target_correlation = correlation_df.corr()[target_attribute]

    for attribute, correlation in target_correlation.items():
        if attribute == target_attribute:
            continue

        if abs(correlation) > 0.2:
            if correlation > 0:
                phrases.append(
                    f"There is a positive correlation of {correlation:.2f} between {target_attribute} and {attribute}."
                )
            else:
                phrases.append(
                    f"There is a negative correlation of {correlation:.2f} between {target_attribute} and {attribute}."
                )

    return phrases


dataframe = _prepare_correlation_data()
print("Correlation matrix:")
correlation_matrix = dataframe.corr().round(2)

reading_influence_phrases = _phrased_correlation_data(correlation_matrix, "Reading")