import pandas as pd
from backend.habitlens.utils import obtain_mock_dataframe


def phrased_correlation_insights(
    df: pd.DataFrame, target_attribute: str, threshold: float = 0.01
) -> list[str]:
    numeric_df = df.select_dtypes(include="number")
    if target_attribute not in numeric_df.columns:
        return []

    correlations = numeric_df.corr().round(2)[target_attribute]
    insights = []

    for col, value in correlations.items():
        if col == target_attribute or pd.isna(value):
            continue
        if abs(value) >= threshold:
            direction = "positive" if value > 0 else "negative"
            insights.append(
                f"There is a {direction} correlation of {value:.2f} between '{target_attribute}' and '{col}'."
            )

    return insights


def obtain_data_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include="number").corr().round(2)


if __name__ == "__main__":
    dataframe = obtain_mock_dataframe()
    phrases = phrased_correlation_insights(dataframe, target_attribute="Productivity Score")

    for phrase in phrases:
        print(phrase)
