---
id: "01KJ2T00V6D6VZF6FZNGJ94W1D"
name: "system_executes_pending_data_update_scripts"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/workers/data_update_worker.rb`
- `app/models/data_update_script.rb`
- `spec/workers/data_update_worker_spec.rb` (Test)
- `spec/models/data_update_script_spec.rb` (Test)

## Functional Overview

The system discovers and runs pending data migration scripts stored under `lib/data_update_scripts/`. `DataUpdateScript` tracks every script file on disk as an `ApplicationRecord` row and exposes an ordered list of those still in the `enqueued` state. `DataUpdateWorker`, a high-priority Sidekiq job, iterates over that list (or targets a single script by id), transitions each record through `working` → `succeeded` or `failed`, loads the corresponding Ruby file at runtime, instantiates its class, and calls `run`. After each transition the worker emits a structured log line and a `data_update_scripts.status` metric to the stats client, and reports failures to Honeybadger.

## Design Intent

Scripts are identified by a timestamped filename (e.g. `20200214151804_<name>.rb`) that doubles as their natural sort key, ensuring migrations always execute in creation order. Inserting new scripts via `insert_all` avoids duplicate rows for files that already have a record, making discovery idempotent across repeated job invocations.

## Key Members

- `DataUpdateScript::STATUSES` — `{ enqueued: 0, working: 1, succeeded: 2, failed: 3 }` — lifecycle enum values
- `DataUpdateScript::DIRECTORY` — `lib/data_update_scripts/` — root directory scanned for script files
- `DataUpdateScript::NAMESPACE` — `"DataUpdateScripts"` — Ruby module under which each script class must be defined
- `DataUpdateWorker` — Sidekiq job with `queue: :high_priority, retry: 5`

## Scenarios

### Running all pending scripts (no id given)

1. The worker receives no argument when `perform` is called.
2. `DataUpdateScript.scripts_to_run` scans the scripts directory for `.rb` files, inserts any files not yet recorded in the database (idempotently via `insert_all`), then returns all records with `enqueued` status ordered by filename ascending.
3. For each script the worker transitions the record to `working` and emits a log line and stats metric.
4. The worker requires the script file, instantiates the class resolved from its filename, and calls `run`.
5. On success, the record transitions to `succeeded`; the worker logs and increments the metric again.
6. Scripts that were already processed (not in `enqueued` state) are not included and are not re-executed.

### Running a single script by id

1. The worker receives a specific `DataUpdateScript` id.
2. It loads the record with `DataUpdateScript.find(id)` — no discovery step occurs.
3. The record is transitioned to `working` and metrics are emitted.
4. The script file is required, the class is instantiated, and `run` is called.
5. On success the record transitions to `succeeded` and status is logged and metered.

### Checking whether any scripts remain to be run

1. A caller invokes `DataUpdateScript.scripts_to_run?`.
2. The method reads all `file_name` and `status` pairs from the database.
3. It returns `true` if the number of files on disk exceeds the number of database rows, or if any existing row has status `enqueued`.
4. It returns `false` if every database row is in `working`, `succeeded`, or `failed` status and no new files have appeared.

## Failures / Exceptions

- If a script raises `StandardError` during `run`, `mark_as_failed!` records the exception class and message in the `error` column and sets `finished_at`, `status` transitions to `failed`. The worker logs the failure at error level, increments the stat metric with `status:failed`, and notifies Honeybadger with the script id as context. Execution continues for any remaining scripts.
