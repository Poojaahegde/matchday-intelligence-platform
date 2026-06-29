import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "apps" / "api"))

from app.services.analytics import summarize, momentum  # noqa: E402
from app.models.entities import EventType  # noqa: E402


class FakeEvent:
    def __init__(self, minute, type_, team_id=1, detail=None):
        self.minute = minute
        self.type = EventType(type_)
        self.team_id = team_id
        self.detail = detail


def test_summarize_counts_goals_and_shots():
    events = [
        FakeEvent(10, "goal", 1),
        FakeEvent(20, "shot", 1),
        FakeEvent(25, "shot_on_target", 2),
    ]
    s = summarize(events)
    assert s["goals"][1] == 1
    assert s["shots"][2] == 1
    assert s["shots_on_target"][2] == 1


def test_momentum_orders_by_minute_and_weights():
    events = [FakeEvent(30, "shot", 1), FakeEvent(10, "goal", 1)]
    m = momentum(events)
    assert m[0]["minute"] == 10
    assert m[0]["weight"] == 5


def test_possession_parsed_from_detail():
    events = [FakeEvent(30, "possession", 1, detail="58")]
    s = summarize(events)
    assert s["possession"][1] == 58.0
