# Interview notes

Questions I expect about this project, and how I would answer them. These are
prompts for me, not a script.

## Design

- Why separate the read path, write path, and live-update path? What would break
  if I merged them?
- Why is the analytics module pure? What does that buy me in testing and reuse?
- Why Redis pub/sub instead of writing straight to the WebSocket? What are the
  delivery guarantees, and where does this fall short?
- Why one wide `match_events` table instead of a table per event type?

## Tradeoffs

- I use `create_all` instead of migrations. When is that fine, and when is it
  dangerous? What is my migration plan?
- The momentum score is a flat weighted sum. What are its blind spots versus an
  xG model?
- Possession is stored as snapshots. What did that simplify, and what does it
  cost me?

## Reliability

- What happens when Redis is down? Walk through the fallback.
- How do I avoid a 500 on an unknown match id or a bad token?
- If two operators submit events at the same minute, what happens?

## Scaling

- Where is the first bottleneck if traffic grows? (Hint: analytics recompute
  on every request.)
- How would I cache analytics, and how would I invalidate the cache?
- How would I run multiple API instances given the WebSocket subscriptions?

## Testing

- Why can the analytics tests run without a database?
- What do the CI Postgres and Redis services cover that the unit tests do not?
- What is the highest-value test I have not written yet? (The Playwright
  end-to-end test in the roadmap.)

## If I had more time

- Per-operator auth, Alembic migrations, a reconnecting WebSocket client, and a
  cache in front of the analytics endpoints.
