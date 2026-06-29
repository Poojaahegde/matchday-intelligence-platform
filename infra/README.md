# Infra

Local development uses Docker Compose only (`docker-compose.yml` at the repo
root). There is no cloud infrastructure-as-code yet.

Services:

- `db` — Postgres 16, data persisted in the `dbdata` volume.
- `redis` — Redis 7 for the live-update pub/sub channel.
- `api` — the FastAPI service, built from `apps/api/Dockerfile`.
- `web` — the Next.js dashboard, built from `apps/web/Dockerfile`.

If I deployed this, the first additions here would be a managed Postgres, a
managed Redis, and a small Terraform module to provision them.
