---
id: "01KJ2SZQQG4JYPHKNCN2BSNYMN"
name: "admin_can_force_run_data_update_script"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/admin/data_update_scripts_controller.rb`
- `app/models/data_update_script.rb`
- `app/workers/data_update_worker.rb`
- `app/javascript/admin/controllers/data_update_script_controller.js`
- `spec/requests/admin/data_update_scripts_spec.rb` (Test)
- `spec/workers/data_update_worker_spec.rb` (Test)
- `app/javascript/admin/__tests__/controllers/data_update_script_controller.test.js` (Test)

## Functional Overview

Tech admins can manually trigger re-execution of a specific data update script from the admin panel. When an admin clicks the "Re-run" button next to a script, the browser sends a POST request to `POST /admin/advanced/data_update_scripts/:id/force_run`, which enqueues `DataUpdateWorker` with the script's ID. The worker finds the corresponding `DataUpdateScript` record, transitions its status to `working`, executes the script file, and marks it as `succeeded` or `failed`. The browser then polls `GET /admin/advanced/data_update_scripts/:id` every second (up to 20 attempts) to detect when the script reaches a terminal status and updates the table row in place. Only authenticated users with internal tech-admin access may trigger this action.

## Design Intent

Polling is capped at 20 attempts (approximately 20 seconds) to avoid indefinite waiting for scripts that may take a long time. After the cap, an informational banner advises the admin to refresh the page manually. This keeps the UI responsive without requiring WebSockets or server-sent events.

## Key Members

- `DataUpdateScript::STATUSES` — enum: `enqueued: 0`, `working: 1`, `succeeded: 2`, `failed: 3`
- `DataUpdateWorker` — Sidekiq job on the `high_priority` queue with up to 5 retries
- `url` (Stimulus value) — base URL used to build the `force_run` and status-check endpoints

## Scenarios

### Admin force-runs a script successfully

1. A tech admin views the data update scripts index and sees a script with status `failed` and a "Re-run" button.
2. The admin clicks "Re-run"; the browser immediately shows a loading indicator in the status and run-at columns.
3. The browser POSTs to `POST /admin/advanced/data_update_scripts/:id/force_run`; the server enqueues `DataUpdateWorker` with the script ID and returns a success response.
4. The browser begins polling `GET /admin/advanced/data_update_scripts/:id` every second.
5. The worker finds the script, marks it as `working`, executes the script file, then marks it as `succeeded`.
6. The next poll receives `succeeded`; the browser updates the status and run-at columns, removes the `alert-danger` class from the row, and removes the "Re-run" button.

### Admin force-runs a script that fails during execution

1. The admin triggers a force-run as described above; `DataUpdateWorker` is enqueued.
2. The worker marks the script as `working`, then encounters an error during execution.
3. The worker records the error message, marks the script as `failed`, logs an error-level message, and notifies Honeybadger.
4. The next successful poll returns `failed` with an error description; the browser renders the error text beneath the status in the table row.

### Force-run request itself fails (HTTP error response)

1. The admin clicks "Re-run" but the POST to `force_run` returns a non-OK HTTP response (e.g., server error).
2. The browser skips polling and immediately shows an error banner with the message "{filename} - Something went wrong." and clears the loading indicators.

### Polling times out before a terminal status is reached

1. After triggering a force-run, the browser polls for status up to 20 times (one per second) without receiving `succeeded` or `failed`.
2. On the 21st interval tick, polling stops and an informational banner advises the admin that the script may take some time and to refresh the page to check the status.

### Non-tech-admin user attempts to access the endpoint

1. A regular authenticated user requests any data update scripts endpoint.
2. Authorization via `InternalPolicy#access?` raises an error and the request is blocked.

## Failures / Exceptions

- If `DataUpdateScript.find` raises `ActiveRecord::RecordNotFound` in the `show` action, the controller returns a JSON error with HTTP `404 Not_Found`.
- If the script file raises `StandardError` during worker execution, the error is caught, the script is marked `failed` with the error class and message stored, and the error is reported to Honeybadger.
- If a poll request returns a non-OK response, the browser shows an error banner with the script ID and the server-provided error message, and polling terminates.
