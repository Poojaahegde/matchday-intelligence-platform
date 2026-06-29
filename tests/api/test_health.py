import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "apps" / "api"))

# These tests exercise the analytics contract without a live DB. Full HTTP
# tests run in CI where a Postgres service is available (see ci.yml).
from app.services.analytics import summarize  # noqa: E402


def test_summary_keys_present():
    s = summarize([])
    for key in ("goals", "shots", "shots_on_target", "possession", "cards"):
        assert key in s


def test_empty_events_have_no_goals():
    s = summarize([])
    assert s["goals"] == {}
