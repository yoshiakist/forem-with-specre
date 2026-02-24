---
id: "01KJ75D28S88YETAPX6NF3ZP4C"
name: "system_purges_old_email_delivery_records"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/email_message.rb` (shared with admin_can_view_sent_email_messages)
- `app/workers/emails/remove_old_emails_worker.rb`
- `spec/workers/emails/remove_old_emails_worker_spec.rb` (Test)

## Functional Overview

The system periodically purges old email delivery records from the ahoy_messages table to prevent unbounded growth. A background worker invokes the purge on a scheduled basis, deleting records older than two months in batches of up to 50,000 rows per execution. Records that are linked to a feedback message — indicating they were sent manually by a human admin — are unconditionally retained, as they serve an audit purpose. All other delivery records are eligible for removal once they exceed the retention threshold.

## Design Intent

Admin-sent emails tied to feedback messages are preserved for audit and accountability purposes, since they represent deliberate human actions rather than automated system notifications. The batch-delete approach (LIMIT 50,000 per query) limits database lock contention and query duration, making the purge safe to run on large tables without degrading production performance. The worker is placed on the low-priority queue to further reduce operational impact.

## Key Members

- `EmailMessage.fast_destroy_old_retained_email_deliveries(destroy_before_timestamp)` — Class method that deletes ahoy_messages records older than the given timestamp, excluding any rows with a non-NULL `feedback_message_id`. Defaults to 2 months ago.
- `BulkSqlDelete.delete_in_batches(sql)` — Executes the delete SQL in repeated batches until no rows remain.
- `Emails::RemoveOldEmailsWorker#perform` — Sidekiq job entry point; calls the purge method with the default threshold.
- Sidekiq options: queue `low_priority`, retry `10`.

## Scenarios

### Normal purge of old automated email records

1. The scheduler enqueues `Emails::RemoveOldEmailsWorker` on the `low_priority` queue.
2. The worker calls `EmailMessage.fast_destroy_old_retained_email_deliveries` with the default threshold of two months ago.
3. The system selects up to 50,000 rows from `ahoy_messages` where `sent_at` is before the threshold and `feedback_message_id` is NULL.
4. Those rows are deleted in batches until none remain.
5. The job completes successfully.

### Retention of admin-sent emails linked to feedback messages

1. Email delivery records that have a non-NULL `feedback_message_id` are excluded from the delete query regardless of their age.
2. These records persist in `ahoy_messages` after every purge cycle, preserving the audit trail for admin-initiated emails.

### Batch processing limits database load

1. The delete query selects at most 50,000 row IDs per batch using a subquery with LIMIT.
2. `BulkSqlDelete.delete_in_batches` repeats the operation until fewer than 50,000 rows are affected, ensuring no single query locks a large portion of the table.

## Failures / Exceptions

- If the job fails (e.g., database error), Sidekiq retries it up to 10 times before moving it to the dead queue.
- Partial batches deleted before a failure are not rolled back; subsequent retries continue deleting remaining eligible rows.
