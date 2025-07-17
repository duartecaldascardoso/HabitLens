from habitlens.notion_api import get_daily_habits
import pandas as pd

def main():
    dataframe = pd.DataFrame(get_daily_habits())
    dataframe.to_csv("data/habits.csv", index=False)
    print("Exported to data/habits.csv")

if __name__ == "__main__":
    main()