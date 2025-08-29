import random
import pandas as pd
from datetime import datetime, timedelta

MOODS = ["Terrible", "Sad", "Meh", "Neutral", "Good", "Great", "Amazing"]
ENERGY_LEVELS = ["Very Low", "Low", "Medium", "High", "Very High"]
GYM_DAYS = ["Arms Day", "Legs Day", "Chest Day", "Back Day", "Cardio"]
DAY_TYPES = ["Office", "Home office", "Classes", "Weekend", "Vacation"]
GAMES = ["Clash Royale", "Baldur's Gate", "Chess", "Zelda"]
MUSIC = [
    "Bass",
    "Piano",
    "Listening",
    "Composition",
    "Guitar",
    "Vocals",
    "Recording",
    "Practice",
]
CUSTOM_ACTIVITIES = [
    "Work in HabitLens",
    "Cooking",
    "Meditation",
    "Hangout with Cami",
    "Dinner with Cami",
]


def generate_mock_entry(date):
    day_type = (
        "Weekend"
        if date.weekday() >= 5
        else random.choices(DAY_TYPES[:-1], weights=[4, 3, 3, 1])[0]
    )

    mood = random.choices(MOODS, weights=[2, 5, 10, 30, 25, 20, 8])[0]
    productivity_score = random.randint(1, 5)
    energy = random.choices(ENERGY_LEVELS, weights=[5, 15, 40, 30, 10])[0]

    gym_chance = random.random()
    gym = []
    if gym_chance > 0.4:
        gym = random.sample(GYM_DAYS, k=random.randint(1, 2))

    reading = random.random() < 0.6
    sleep_hours = round(random.normalvariate(7, 1.2), 1)
    games = random.sample(GAMES, k=random.randint(0, 2))
    music = random.sample(MUSIC, k=random.randint(0, 3))
    custom = random.sample(CUSTOM_ACTIVITIES, k=random.randint(0, 3))

    return {
        "Date": date.date(),
        "Day": date.strftime("%A"),
        "Mood": mood,
        "Productivity Score": productivity_score,
        "Energy Level": energy,
        "Gym": gym,
        "Day Type": day_type,
        "Reading": reading,
        "Sleep Hours": max(4, min(sleep_hours, 9)),
        "Games Played": games,
        "Music Related": music,
        "Custom Activities": custom,
    }


def generate_mock_data(num_days=3650):
    today = datetime.today()
    data = [generate_mock_entry(today - timedelta(days=i)) for i in range(num_days)]
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_mock_data(3650)
    # Use relative path from project root
    output_path = "backend/habitlens/data/mock_habits.csv"
    df.to_csv(output_path, index=False)
    print(f"Mock data generated and saved. Path: {output_path}")
