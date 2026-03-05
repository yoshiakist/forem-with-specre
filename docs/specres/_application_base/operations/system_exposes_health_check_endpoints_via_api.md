---
id: "01KJXRWB4MV7QFF67TPC93RCNM"
name: "system_exposes_health_check_endpoints_via_api"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/controllers/concerns/api/health_checks_controller.rb`
- `app/controllers/api/v0/health_checks_controller.rb`
- `app/controllers/api/v1/health_checks_controller.rb`
- `spec/requests/api/v0/health_checks_spec.rb` (Test)
- `spec/requests/api/v1/health_checks_spec.rb` (Test)

## Functional Overview

The system exposes three health check endpoints — `/api/health_checks/app`, `/api/health_checks/database`, and `/api/health_checks/cache` — available in both API v0 and v1. Each endpoint responds with a JSON message and an appropriate HTTP status. All requests from non-local origins must supply a valid `health-check-token` header whose value matches the configured `Settings::General.health_check_token`; requests without a valid token receive a 401 Unauthorized response. The shared logic lives in the `Api::HealthChecksController` concern, which is included by the versioned controllers.

## Design Intent

The behavior is extracted into a Rails concern so that both API versions share identical logic without duplication. Token-based authentication guards the endpoints against external probing while still allowing local (loopback) requests to pass through without a token, which is useful for internal monitoring tools running on the same host.

## Scenarios

### App health check succeeds

1. A client sends `GET /api/health_checks/app` with a valid `health-check-token` header (or from a local address).
2. The system responds with HTTP 200 and `{ "message": "App is up!" }`.

### Database health check succeeds

1. A client sends `GET /api/health_checks/database` with a valid token.
2. The system verifies that `ActiveRecord::Base` reports an active connection.
3. The system responds with HTTP 200 and `{ "message": "Database connected" }`.

### Database health check fails

1. A client sends `GET /api/health_checks/database` with a valid token.
2. The database connection check returns false.
3. The system responds with HTTP 500 and `{ "message": "Database NOT connected!" }`.

### Cache health check succeeds

1. A client sends `GET /api/health_checks/cache` with a valid token.
2. The system pings every configured Redis URL (`REDIS_URL`, `REDIS_SESSIONS_URL`, `REDIS_SIDEKIQ_URL`, `REDIS_RPUSH_URL`); all respond with `PONG`.
3. The system responds with HTTP 200 and `{ "message": "Redis connected" }`.

### Cache health check fails

1. A client sends `GET /api/health_checks/cache` with a valid token.
2. At least one Redis instance fails to respond with `PONG`.
3. The system responds with HTTP 500 and `{ "message": "Redis NOT connected!" }`.

## Failures / Exceptions

- A request originating from a non-local IP without a `health-check-token` header, or with a token that does not match `Settings::General.health_check_token`, receives HTTP 401 Unauthorized.
- If no Redis URLs are configured in the environment, `all_cache_instances_connected?` returns true (the `.compact.all?` on an empty array vacuously succeeds), so the cache endpoint reports healthy.
