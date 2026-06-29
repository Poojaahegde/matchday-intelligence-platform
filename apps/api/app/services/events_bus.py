"""Thin pub/sub over Redis so WebSocket clients get live event pushes.

Falls back to a no-op bus if Redis is unavailable, which keeps local dev and
unit tests from requiring a running Redis.
"""
import json

try:
    import redis  # type: ignore
except ImportError:  # pragma: no cover
    redis = None

from ..config import settings

CHANNEL_PREFIX = "match:"


class EventBus:
    def __init__(self):
        self._client = None
        if redis is not None:
            try:
                self._client = redis.from_url(settings.redis_url)
                self._client.ping()
            except Exception:
                self._client = None

    def publish(self, match_id: int, payload: dict) -> None:
        if self._client:
            self._client.publish(CHANNEL_PREFIX + str(match_id), json.dumps(payload))

    def subscribe(self, match_id: int):
        if not self._client:
            return None
        pubsub = self._client.pubsub()
        pubsub.subscribe(CHANNEL_PREFIX + str(match_id))
        return pubsub


bus = EventBus()
