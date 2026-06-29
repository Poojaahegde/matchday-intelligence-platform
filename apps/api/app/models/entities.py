from datetime import datetime
import enum

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship

from ..db import Base


class EventType(str, enum.Enum):
    goal = "goal"
    assist = "assist"
    yellow_card = "yellow_card"
    red_card = "red_card"
    substitution = "substitution"
    shot = "shot"
    shot_on_target = "shot_on_target"
    possession = "possession"


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    players = relationship("Player", back_populates="team")


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="players")


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    status = Column(String, default="scheduled")
    kickoff = Column(DateTime, default=datetime.utcnow)
    events = relationship("MatchEvent", back_populates="match",
                          cascade="all, delete-orphan")


class MatchEvent(Base):
    __tablename__ = "match_events"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    minute = Column(Integer, nullable=False)
    type = Column(Enum(EventType), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    detail = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    match = relationship("Match", back_populates="events")
