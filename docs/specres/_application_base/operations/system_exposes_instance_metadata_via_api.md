---
id: "01KJXRX5G28PGJCPGX88ZW6NK0"
name: "system_exposes_instance_metadata_via_api"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/controllers/concerns/api/instances_controller.rb`
- `app/controllers/api/v0/instances_controller.rb`
- `app/controllers/api/v1/instances_controller.rb`
- `spec/requests/api/v0/instances_spec.rb` (Test)
- `spec/requests/api/v1/instances_spec.rb` (Test)

## Functional Overview

The system exposes a public read-only API endpoint (`GET /api/instance`) available in both V0 and V1 that returns metadata describing the current Forem instance. The response includes community settings such as name, description, tagline, domain, logo and cover image URLs, Forem context, directory display preference, release version, and visibility state. Both versioned controllers share identical logic via the `Api::InstancesController` concern. When the instance is public, the response also sets cache-control headers with a 600-second TTL to enable edge caching.

## Design Intent

The shared concern pattern (`Api::InstancesController`) avoids duplicating the `show` action between V0 and V1. Both versioned controllers mix it in, allowing a single source of truth for this metadata contract while each versioned controller can independently set other before-actions (here, `set_no_cache_header`). Cache headers are set only for public instances to avoid caching responses that contain potentially sensitive visibility state.

## Key Members

- `visibility` — derived from two settings: returns `"pending"` if the instance has no users yet, `"public"` or `"private"` based on `Settings::UserExperience.public`.
- `release_version` — reads `.release-version` from the Rails root; falls back to an `edge.<YYYYMMDD>.0` string derived from the most recently modified application file.

## Scenarios

### Returning instance metadata to an authenticated or anonymous caller

1. A client sends `GET /api/instance` (optionally with the V1 `Accept` header).
2. The system reads community and general settings from `Settings::Community`, `Settings::General`, and `Settings::UserExperience`.
3. The system determines the release version from the `.release-version` file.
4. The system responds with HTTP 200 and a JSON object containing `context`, `cover_image_url`, `description`, `display_in_directory`, `domain`, `logo_image_url`, `name`, `tagline`, `version`, and `visibility`.

### Reporting visibility as public

1. The instance is configured as public and at least one user exists.
2. The system sets `visibility` to `"public"` in the response.
3. The system additionally writes Surrogate-Control cache headers with a 600-second max-age to support edge caching.

### Reporting visibility as private

1. The instance is configured as non-public and at least one user exists.
2. The system sets `visibility` to `"private"` in the response.
3. No cache-control headers are written.

### Reporting visibility as pending

1. The instance has no users yet (`waiting_on_first_user` is true).
2. The system sets `visibility` to `"pending"` regardless of the public/private setting.

## Failures / Exceptions

- If the `.release-version` file is absent or unreadable, the system falls back to scanning all files under `app`, `config`, `db`, and `lib`, derives the most recent modification timestamp, and returns a version string in the form `edge.<YYYYMMDD>.0`.
