"""Turns a flat list of match events into the numbers the dashboard needs."""
from collections import defaultdict
from typing import Iterable


def summarize(events: Iterable) -> dict:
    goals = defaultdict(int)
    shots = defaultdict(int)
    shots_on_target = defaultdict(int)
    possession = {}
    cards = defaultdict(lambda: {"yellow": 0, "red": 0})

    for e in events:
        t = e.team_id
        if e.type.value == "goal":
            goals[t] += 1
        elif e.type.value == "shot":
            shots[t] += 1
        elif e.type.value == "shot_on_target":
            shots_on_target[t] += 1
            shots[t] += 1
        elif e.type.value == "possession" and e.detail:
            try:
                possession[t] = float(e.detail)
            except ValueError:
                pass
        elif e.type.value == "yellow_card":
            cards[t]["yellow"] += 1
        elif e.type.value == "red_card":
            cards[t]["red"] += 1

    return {
        "goals": dict(goals),
        "shots": dict(shots),
        "shots_on_target": dict(shots_on_target),
        "possession": possession,
        "cards": {k: v for k, v in cards.items()},
    }


def momentum(events: Iterable) -> list:
    """Rolling attacking-intent score per minute, used by the momentum chart."""
    weights = {"goal": 5, "shot_on_target": 3, "shot": 1}
    timeline = []
    for e in sorted(events, key=lambda x: x.minute):
        w = weights.get(e.type.value, 0)
        if w:
            timeline.append({"minute": e.minute, "team_id": e.team_id, "weight": w})
    return timeline
