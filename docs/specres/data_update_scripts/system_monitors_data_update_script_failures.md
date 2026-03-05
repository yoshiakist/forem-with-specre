---
id: "01KJ2T2BMXGZ8AEC4TF9PCZH99"
name: "system_monitors_data_update_script_failures"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/workers/metrics/check_data_update_script_statuses.rb`
- `spec/workers/metrics/check_data_update_script_statuses_spec.rb` (Test)

## Functional Overview

A low-priority Sidekiq background job periodically checks for data update scripts that have recently failed. On each run it queries `DataUpdateScript.failed` limited to scripts created within the past 24 hours, then emits a count metric for every matching script via `ForemStatsClient` under the key `"data_update_scripts.failures"`, tagging each metric with the script's file name. This allows the platform's metrics system to track and alert on data update script failures in near-real-time without impacting higher-priority work.

## Design Intent

Failures older than 24 hours are excluded from each run, so the metric represents only recent failures. This avoids double-counting failures across multiple job executions while ensuring that a failure that occurred just before the job ran is still captured.

## Scenarios

### Recently failed scripts are reported

1. The job is enqueued on the `low_priority` queue with up to 10 retries.
2. On `perform`, the system queries `DataUpdateScript.failed` filtered to records created within the last 24 hours.
3. For each matching script, the system sends a count of 1 to `ForemStatsClient` with metric key `"data_update_scripts.failures"` and a tag of `file_name:<script_file_name>`.

### Scripts that failed more than 24 hours ago are ignored

1. A `DataUpdateScript` record with `status: :failed` and `created_at` older than 24 hours exists.
2. The job's time-window filter excludes it from the query result.
3. No metric is emitted for that script.

### Non-failed scripts are not reported

1. A `DataUpdateScript` record with a status other than `failed` exists.
2. `DataUpdateScript.failed` does not include it in the result set.
3. No metric is emitted for that script.
