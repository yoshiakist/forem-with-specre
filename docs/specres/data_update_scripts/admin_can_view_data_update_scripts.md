---
id: "01KJ2SZCDD0QR1BVHSPYKQZ955"
name: "admin_can_view_data_update_scripts"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/admin/data_update_scripts_controller.rb`
- `app/models/data_update_script.rb`
- `app/views/admin/data_update_scripts/index.html.erb` (Template)
- `app/javascript/admin/controllers/data_update_script_controller.js`
- `spec/requests/admin/data_update_scripts_spec.rb` (Test)
- `spec/routing/data_update_scripts_admin_routes_spec.rb` (Test)
- `spec/models/data_update_script_spec.rb` (Test)
- `app/javascript/admin/__tests__/controllers/data_update_script_controller.test.js` (Test)

## Functional Overview

Tech admins can view a list of all data update scripts in the admin panel, showing each script's ID, filename, creation time, last run time, and current status. The index page renders scripts sorted by `run_at` descending. Scripts with a `failed` status are visually highlighted and display a "Re-run" button. When an admin clicks "Re-run", the Stimulus controller (`DataUpdateScriptController`) immediately shows a loading state, then posts to the `force_run` endpoint to enqueue the script via `DataUpdateWorker`. It subsequently polls the `show` endpoint every second (up to 20 times) until the script reaches a terminal status (`succeeded` or `failed`), updating the table row in place. On success, the danger styling and Re-run button are removed. The admin route is gated by a feature flag (`data_update_scripts`) and requires the `InternalPolicy` `access?` authorization, restricting access to tech admins only.

## Design Intent

Polling rather than a WebSocket approach is used for simplicity: the frontend polls the `show` JSON endpoint (which leverages the existing REST resource) at one-second intervals after triggering a force run. A maximum of 20 polls prevents indefinite waiting; if the script has not finished, an informational banner is shown asking the admin to refresh the page manually.

## Key Members

- `STATUSES` — enum mapping `enqueued: 0`, `working: 1`, `succeeded: 2`, `failed: 3`; controls all status transitions in the model
- `urlValue` — Stimulus value holding the base URL (`admin/advanced/data_update_scripts`) used to build `show` and `force_run` fetch URLs

## Scenarios

### Viewing the list as a tech admin

1. A user with tech admin privileges navigates to `GET /admin/advanced/data_update_scripts` while the `data_update_scripts` feature flag is enabled.
2. The controller loads all `DataUpdateScript` records ordered by `run_at` descending and renders the index template.
3. The table shows each script's ID, filename, created-at timestamp, run-at timestamp, and status. Scripts with `failed` status are highlighted in red and show a "Re-run" button.

### Fetching a single script as JSON

1. The Stimulus controller (or any client) sends `GET /admin/advanced/data_update_scripts/:id`.
2. The controller finds the record by ID and returns it as JSON under the `response` key.
3. If no record exists for the given ID, the controller returns a `404` JSON response with an `error` key describing the `ActiveRecord::RecordNotFound` exception.

### Force-running a failed script

1. An admin clicks the "Re-run" button next to a failed script.
2. The Stimulus controller immediately blanks the status column and shows "loading.." in the run-at column.
3. It sends `POST /admin/advanced/data_update_scripts/:id/force_run`, which enqueues the script via `DataUpdateWorker`.
4. If the POST fails (non-2xx), an error banner is displayed with the script filename and "Something went wrong."
5. On a successful POST, the controller begins polling `GET /admin/advanced/data_update_scripts/:id` every second.

### Polling for updated script status

1. After a successful force-run request, the Stimulus controller polls the `show` endpoint at one-second intervals.
2. When the response shows a terminal status (`succeeded` or `failed`), polling stops and the table row is updated with the new `run_at` and `status` values.
3. If the script `failed`, any associated error message is rendered below the status in the table cell.
4. If the script `succeeded`, the red danger styling is removed from the row and the "Re-run" button is removed.
5. If 20 polls complete without a terminal status, polling stops and an informational banner informs the admin that the script may take more time and to refresh the page.

### Access control for non-tech admins

1. A user without tech admin privileges attempts to access `GET /admin/advanced/data_update_scripts`.
2. The `authorize_admin` before-action calls `InternalPolicy#access?`, which raises an authorization error.
3. The request is blocked and an error is raised.

## Failures / Exceptions

- `ActiveRecord::RecordNotFound` on `GET /admin/advanced/data_update_scripts/:id` returns `{ error: "ActiveRecord::RecordNotFound: ..." }` with HTTP `404`.
- A non-2xx response from `POST force_run` triggers `setErrorBanner` with "Something went wrong."
- A non-2xx response from `GET show` during polling triggers `setErrorBanner` with the script ID and the JSON error message.
- After 20 failed poll attempts, `setErrorBanner` is called with an informational message asking the admin to refresh manually.
