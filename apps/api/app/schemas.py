from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventIn(BaseModel):
    minute: int
    type: str
    team_id: Optional[int] = None
    player_id: Optional[int] = None
    detail: Optional[str] = None


class EventOut(EventIn):
    id: int
    match_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MatchOut(BaseModel):
    id: int
    home_team_id: int
    away_team_id: int
    status: str

    class Config:
        from_attributes = True
