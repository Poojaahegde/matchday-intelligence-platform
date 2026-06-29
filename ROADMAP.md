# Roadmap

These are the next things I would build, written as the GitHub issues I would
open. They are ordered roughly by impact.

## 1. Add Alembic migrations
Replace `create_all` with versioned migrations so schema changes are safe in
shared environments. Acceptance: a documented `alembic upgrade head` step.

## 2. Per-operator authentication
Swap the single shared admin token for accounts with hashed passwords and
session tokens, so multiple operators can be audited separately.

## 3. Expected-goals (xG) momentum model
Replace the flat weighted-event momentum score with a shot-quality model so the
momentum chart reflects chance quality, not just shot count.

## 4. Continuous possession time series
Store possession as a sampled series and render it as a stacked area chart
instead of discrete snapshots.

## 5. Formation view
Add a pitch component that places players by position and updates on
substitutions. Needs a lineup endpoint.

## 6. Cache analytics responses
Add Redis caching with invalidation on new events so large historical matches
do not recompute on every request.

## 7. Social summary image export
Render the post-match summary to a shareable PNG card, not just text.

## 8. Reconnecting WebSocket client
Make the dashboard auto-reconnect with backoff and replay missed events on
reconnect.

## 9. Match archive search and filters
Add pagination, team filters, and date filters to the historical match list.

## 10. End-to-end test with Playwright
Add a browser test that seeds a match, adds a live event via the admin page,
and asserts the dashboard updates over the WebSocket.
