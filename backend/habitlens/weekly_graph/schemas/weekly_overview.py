from pydantic import BaseModel, Field


class WeeklyOverview(BaseModel):
    """An overview used to explain the events of the week with structured fields for better Notion reporting."""

    weekly_summary: str = Field(description="Summary of the data from the last two weeks.")

    key_observations: str = Field(
        description="Key patterns and correlations identified from the data."
    )

    improvement_areas: str = Field(
        description="Areas where the user could improve based on the data analysis."
    )

    habit_recommendations: str = Field(
        description="Specific habit recommendations based on data correlations."
    )
