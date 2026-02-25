---
id: "01KJ9R39KP2S3HPPX5GYS7WD2T"
name: "system_deletes_user_account_data"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/workers/users/delete_worker.rb`
- `app/services/users/delete.rb`
- `spec/workers/users/delete_worker_spec.rb` (Test)

## Functional Overview

When a user account deletion is requested, `Users::DeleteWorker` is a high-priority Sidekiq job that orchestrates the full deletion sequence. It locates the user by ID, delegates the actual data removal to `Users::Delete`, then creates a `GDPRDeleteRequest` record so admins can follow up on any residual GDPR-regulated data. If the deletion was not triggered by an admin and the user has an email address on file, it delivers an `account_deleted_email` via `NotifyMailer` to inform the former user. Any unhandled error is reported to ForemStatsClient and Honeybadger without re-raising, keeping the job's retry behaviour predictable.

## Design Intent

The worker separates scheduling (Sidekiq job) from deletion logic (`Users::Delete` service) so the heavy lifting can be tested and reused independently. GDPR compliance is handled unconditionally — the request record is always created regardless of who triggered the deletion — while the confirmation email is suppressed for admin-initiated deletions to avoid confusing former users about the cause. Errors are caught and surfaced to monitoring rather than swallowed silently, allowing the retry policy to take effect without losing observability.

## Key Members

- `user_id: Integer` — the database ID of the user to be deleted; looked up with `find_by` so a missing record causes a no-op rather than a crash
- `admin_delete: Boolean` — when `true`, suppresses the confirmation email (defaults to `false`)

## Scenarios

### User is found and deleted by a regular (non-admin) trigger

1. The job receives a valid user ID and `admin_delete` flag set to `false`.
2. The user record is located in the database.
3. `Users::Delete` is called with the user object, which removes all associated data.
4. A `GDPRDeleteRequest` record is created with the user's ID, email, and username.
5. Because `admin_delete` is false and the user has an email address, `NotifyMailer` delivers an `account_deleted_email` to the former user's address.

### User is deleted via an admin-triggered action

1. The job receives a valid user ID and `admin_delete` set to `true`.
2. The user is located, and `Users::Delete` is invoked to remove all data.
3. A `GDPRDeleteRequest` record is created as usual.
4. Email delivery is skipped because `admin_delete` is `true`.

### User ID does not correspond to an existing record

1. The job receives a user ID that does not match any record (e.g., already deleted or invalid).
2. `find_by` returns `nil`; the job returns immediately without further action.
3. No deletion, no GDPR record, and no email are created.

## Failures / Exceptions

- If any `StandardError` is raised during deletion, the worker increments the `users.delete` counter in ForemStatsClient tagged with `action:failed` and the user ID, sets Honeybadger context with the user ID, and notifies Honeybadger with the exception. The error is not re-raised, so Sidekiq's built-in retry mechanism governs subsequent attempts (up to 10 retries on the `high_priority` queue).
