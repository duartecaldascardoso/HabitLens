from pydantic import BaseModel, Field


class WeeklyOverview(BaseModel):
    """An overview used to explain the events of the week. Used to summarize and find enhancements."""

    weekly_summary: str = Field(description="Summary of the data from the last week.")

    activity_suggestion: str = Field(description="Suggestion of an activity for the next week.")


