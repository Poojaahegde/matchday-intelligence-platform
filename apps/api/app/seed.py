"""Loads data/sample_match.json into the database for demos."""
import json
import pathlib

from .db import Base, engine, SessionLocal
from .models import Team, Player, Match, MatchEvent

SAMPLE = pathlib.Path(__file__).resolve().parents[2] / "data" / "sample_match.json"


def run():
    Base.metadata.create_all(bind=engine)
    data = json.loads(SAMPLE.read_text())
    db = SessionLocal()
    if db.query(Team).count():
        print("Data already present, skipping seed.")
        return
    teams = {}
    for t in data["teams"]:
        team = Team(name=t["name"])
        db.add(team)
        db.flush()
        teams[t["name"]] = team.id
        for p in t["players"]:
            db.add(Player(name=p["name"], position=p.get("position"),
                          team_id=team.id))
    home, away = data["match"]["home"], data["match"]["away"]
    match = Match(home_team_id=teams[home], away_team_id=teams[away],
                  status="finished")
    db.add(match)
    db.flush()
    for e in data["events"]:
        db.add(MatchEvent(match_id=match.id, minute=e["minute"],
                          type=e["type"], team_id=teams.get(e.get("team")),
                          detail=e.get("detail")))
    db.commit()
    print(f"Seeded match {match.id} with {len(data['events'])} events.")


if __name__ == "__main__":
    run()
