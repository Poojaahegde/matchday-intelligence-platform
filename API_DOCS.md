# API reference

Base URL in local dev: `http://localhost:8000`. FastAPI also serves interactive
docs at `/docs` (Swagger) and `/redoc`.

All write endpoints require the `X-Admin-Token` header matching `ADMIN_API_TOKEN`.

## GET /health

Liveness probe.

```json
{ "status": "ok" }
```

## GET /matches

Returns every match.

```bash
curl http://localhost:8000/matches
```

## GET /matches/{id}

Returns one match, or 404 if it does not exist.

## GET /matches/{id}/events

Ordered list of events for a match (earliest minute first).

## GET /matches/{id}/analytics

Computed summary plus the momentum timeline.

```json
{
  "summary": {
    "goals": {"1": 2, "2": 1},
    "shots": {"1": 3, "2": 1},
    "shots_on_target": {"1": 1, "2": 1},
    "possession": {"1": 58.0},
    "cards": {"2": {"yellow": 1, "red": 0}}
  },
  "momentum": [
    {"minute": 5, "team_id": 1, "weight": 1}
  ]
}
```

## GET /matches/{id}/report

Post-match report as markdown plus a one-line social summary.

## POST /admin/matches/{id}/events

Adds an event and publishes it to subscribers. Requires the admin token.

Request body:

```json
{ "minute": 90, "type": "goal", "team_id": 1, "detail": "A. Mensah" }
```

Valid `type` values: `goal`, `assist`, `yellow_card`, `red_card`,
`substitution`, `shot`, `shot_on_target`, `possession`. For `possession`,
put the percentage in `detail` (for example `"58"`).

Example:

```bash
curl -X POST http://localhost:8000/admin/matches/1/events \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: $ADMIN_API_TOKEN" \
  -d '{"minute": 90, "type": "goal", "team_id": 1}'
```

Responses: `200` with the created event, `401` for a bad token, `404` for an
unknown match.

## WebSocket /ws/matches/{id}

Connect and the server pushes a JSON frame whenever a new event is written for
that match. Send a periodic text ping to keep the socket open. If Redis is
unavailable the server sends a single info frame and the socket stays idle.
