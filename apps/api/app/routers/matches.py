from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Match, MatchEvent
from ..schemas import MatchOut, EventOut
from ..services.analytics import summarize, momentum

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list[MatchOut])
def list_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()


@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    m = db.get(Match, match_id)
    if not m:
        raise HTTPException(404, "match not found")
    return m


@router.get("/{match_id}/events", response_model=list[EventOut])
def get_events(match_id: int, db: Session = Depends(get_db)):
    return (db.query(MatchEvent)
            .filter(MatchEvent.match_id == match_id)
            .order_by(MatchEvent.minute).all())


@router.get("/{match_id}/analytics")
def get_analytics(match_id: int, db: Session = Depends(get_db)):
    events = db.query(MatchEvent).filter(MatchEvent.match_id == match_id).all()
    return {"summary": summarize(events), "momentum": momentum(events)}


@router.get("/{match_id}/report")
def post_match_report(match_id: int, db: Session = Depends(get_db)):
    m = db.get(Match, match_id)
    if not m:
        raise HTTPException(404, "match not found")
    events = db.query(MatchEvent).filter(MatchEvent.match_id == match_id).all()
    s = summarize(events)
    lines = [f"Full time. Status: {m.status}.",
             f"Goals: {s['goals']}",
             f"Shots: {s['shots']} (on target: {s['shots_on_target']})"]
    return {"markdown": "\n".join(lines), "social": " / ".join(lines)}
