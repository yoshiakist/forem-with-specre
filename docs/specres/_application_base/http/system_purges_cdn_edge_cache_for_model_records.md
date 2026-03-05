---
id: "01KJXTFFGNXAGZ3BW01PEJAA4Z"
name: "system_purges_cdn_edge_cache_for_model_records"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/models/concerns/purgeable.rb`
- `app/models/application_record.rb`
- `spec/models/concerns/purgeable_spec.rb` (Test)

## Functional Overview

The `Purgeable` concern provides every `ApplicationRecord` model with the ability to invalidate Fastly CDN edge-cache entries keyed by either a whole table or an individual record. Class-level methods (`purge_all`, `soft_purge_all`) target the table-level surrogate key, while instance-level methods (`purge`, `soft_purge`) target a per-record key composed of the table name and the record's id. All operations are no-ops when Fastly credentials are absent or when running in the development environment, preventing accidental cache calls during local development. Soft-purge variants mark cached content as stale rather than immediately evicting it, enabling Fastly to serve stale content while revalidating in the background.

## Design Intent

The concern is adapted from the deprecated `fastly-rails` gem's surrogate-key approach. Embedding cache invalidation directly in the model layer ensures that any class inheriting from `ApplicationRecord` gains purge capability without boilerplate. The guard clause that checks for credentials and environment means the behavior is safely inert in non-production environments.

## Key Members

- `table_key` — the surrogate key used to identify all cached responses for an entire model table; equals the database table name
- `record_key` — the surrogate key for a single record; formatted as `"<table_name>/<id>"`
- `FASTLY_API_KEY` / `FASTLY_SERVICE_ID` — application config values that must be present for any purge call to proceed

## Scenarios

### System purges all cached entries for a model table

1. A caller invokes `purge_all` (class method) on a model class.
2. The system verifies that Fastly credentials are configured and the environment is not development.
3. The system calls `purge_by_key` on the Fastly service using the table-level surrogate key, immediately evicting all cached responses tagged with that key.

### System soft-purges all cached entries for a model table

1. A caller invokes `soft_purge_all` (class method) on a model class.
2. The system verifies Fastly credentials and environment as above.
3. The system calls `purge_by_key` with the stale flag set to `true`, marking all table-keyed cache entries as stale without immediate eviction.

### System purges the cached entry for a single record

1. A caller invokes `purge` on a model instance.
2. The system verifies credentials and environment.
3. The system calls `purge_by_key` using the record-level key (`"<table_name>/<id>"`), evicting only that record's cached responses.

### System soft-purges the cached entry for a single record

1. A caller invokes `soft_purge` on a model instance.
2. The system verifies credentials and environment.
3. The system calls `purge_by_key` with the stale flag, marking only the individual record's cache entries as stale.

### System skips purge when Fastly is not configured

1. A caller invokes any purge method (class or instance level).
2. The system detects that either `FASTLY_API_KEY` or `FASTLY_SERVICE_ID` is blank, or that the Rails environment is development.
3. The method returns immediately without contacting Fastly.
