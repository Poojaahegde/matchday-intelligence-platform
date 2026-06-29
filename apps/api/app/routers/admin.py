from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import Match, MatchEvent
from ..schemas import EventIn, EventOut
from ..services.events_bus import bus

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(x_admin_token: str = Header(default="")):
    if x_admin_token != settings.admin_api_token:
        raise HTTPException(401, "invalid admin token")


@router.post("/matches/{match_id}/events", response_model=EventOut,
             dependencies=[Depends(require_admin)])
def add_event(match_id: int, payload: EventIn, db: Session = Depends(get_db)):
    if not db.get(Match, match_id):
        raise HTTPException(404, "match not found")
    event = MatchEvent(match_id=match_id, **payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    bus.publish(match_id, {"event": "match_event", "minute": event.minute,
                           "type": event.type.value})
    return event
