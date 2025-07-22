from typing import Optional
from pydantic import BaseModel

from backend.habitlens.weekly_graph.schemas.sorting_algorithm import WeeklyOverview


class InputWeeklyOverviewState(BaseModel):
    user_identifier: str = "mock_user"
    csv_path: str


class WeeklyOverviewState(InputWeeklyOverviewState):
    week_data: Optional[list] = None
    weekly_overview: Optional[WeeklyOverview] = None
