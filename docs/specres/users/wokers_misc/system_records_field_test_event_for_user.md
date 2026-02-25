---
id: "01KJ9R5J1M1KF820MVS0W4HXK6"
name: "system_records_field_test_event_for_user"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/workers/users/record_field_test_event_worker.rb`
- `spec/workers/users/record_field_test_event_worker_spec.rb` (Test)

## Functional Overview

When a field test conversion event needs to be recorded for a user, this background job looks up the user by ID and delegates the conversion registration to `AbExperiment`. It runs on the low-priority queue with retry support. If the user cannot be found, the job exits silently without performing any action.

## Design Intent

Decoupling the field test event recording from the request cycle via a background job prevents A/B experiment tracking from adding latency to user-facing interactions. The graceful no-op on missing users avoids hard failures for stale or invalidated user references.

## Scenarios

### User exists and goal is provided

1. The job receives a valid user ID and a goal name.
2. The system looks up the user by ID and finds a matching record.
3. The system calls `AbExperiment.register_conversions_for` with the found user and the goal.

### User does not exist

1. The job receives a user ID that does not match any user record (e.g., nil or deleted user).
2. The system attempts to find the user and gets no result.
3. The job exits without calling `AbExperiment.register_conversions_for`.

## Failures / Exceptions

- If the user is not found by the given ID, the job returns early with no side effects and no error raised.
