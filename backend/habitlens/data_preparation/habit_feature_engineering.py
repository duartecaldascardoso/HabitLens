import pandas as pd
import ast


class HabitFeatureEngineer:
    MOOD_SCALE = {
        "Terrible": 0,
        "Sad": 1,
        "Meh": 2,
        "Neutral": 3,
        "Good": 4,
        "Great": 5,
        "Amazing": 6,
    }

    ENERGY_SCALE = {"Very Low": 0, "Low": 1, "Medium": 2, "High": 3, "Very High": 4}

    MULTI_HOT_COLUMNS = [
        "Games Played",
        "Gym",
        "Day Type",
        "Custom Activities",
        "Music Related",
    ]

    def __init__(self, drop_raw_columns: bool = True):
        self.drop_raw_columns = drop_raw_columns

    @staticmethod
    def _parse_list(cell):
        if isinstance(cell, list):
            return cell
        if pd.isna(cell):
            return []
        if isinstance(cell, str):
            try:
                parsed = ast.literal_eval(cell)
                if isinstance(parsed, list):
                    return parsed
                else:
                    return [str(parsed)]
            except Exception:
                return [cell.strip()]
        return [str(cell)]

    @staticmethod
    def _multi_hot_encode(df, col, include_none=False):
        all_items = sorted(set(item for sub in df[col] for item in sub))
        for item in all_items:
            key = f"{col}_{item.replace(' ', '_')}"
            df[key] = df[col].apply(lambda x: int(item in x))

        if include_none:
            df[f"{col}_None"] = df[col].apply(lambda x: int(len(x) == 0))

        return df

    def transform(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        df = df_raw.copy()

        for col in self.MULTI_HOT_COLUMNS:
            if col in df.columns:
                df[col] = df[col].apply(self._parse_list)

        if "Mood" in df.columns:
            df["Mood_Score"] = df["Mood"].map(self.MOOD_SCALE).fillna(-1)
        if "Energy Level" in df.columns:
            df["Energy_Score"] = df["Energy Level"].map(self.ENERGY_SCALE).fillna(-1)

        for col in self.MULTI_HOT_COLUMNS:
            if col in df.columns:
                include_none = col == "Gym"
                df = self._multi_hot_encode(df, col, include_none=include_none)

        if "Reading" in df.columns:
            df["Reading"] = df["Reading"].astype(int)
        if "Sleep Hours" in df.columns:
            df["Sleep Hours"] = pd.to_numeric(
                df["Sleep Hours"], errors="coerce"
            ).fillna(0)
        if "Productivity Score" in df.columns:
            df["Productivity Score"] = pd.to_numeric(
                df["Productivity Score"], errors="coerce"
            )
        if "Nutritional Score" in df.columns:
            df["Nutritional Score"] = pd.to_numeric(
                df["Productivity Score"], errors="coerce"
            )

        if self.drop_raw_columns:
            drop_cols = ["Mood", "Energy Level", "Day"] + self.MULTI_HOT_COLUMNS
            df.drop(
                columns=[col for col in drop_cols if col in df.columns], inplace=True
            )

        return df
