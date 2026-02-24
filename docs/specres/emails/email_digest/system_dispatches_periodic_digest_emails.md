---
id: "01KJ71F6JXM4PY31DJJW0N2R5S"
name: "system_dispatches_periodic_digest_emails"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/email_digest.rb`
- `app/workers/emails/enqueue_digest_worker.rb`
- `spec/services/email_digest_spec.rb` (Test)
- `spec/workers/emails/enqueue_digest_worker_spec.rb` (Test)

## Functional Overview

The system periodically dispatches digest emails to registered users who have opted in to email digests. A scheduled Sidekiq worker (`Emails::EnqueueDigestWorker`) triggers the process by calling `EmailDigest.send_periodic_digest_email`, which queries eligible users and enqueues individual digest delivery workers for each one. Users are fetched in batches and filtered by registration status, active email digest preference, and non-empty email address. On the dev.to community, individual digest jobs are executed inline rather than enqueued asynchronously, as a temporary measure to handle the large user volume; on all other Forem instances, jobs are enqueued normally via Sidekiq. Errors from individual user dispatch attempts are captured and reported to Honeybadger without interrupting the batch.

## Design Intent

The dev.to inline execution path (`Emails::SendUserDigestWorker.new.perform`) is explicitly temporary, added to avoid overwhelming the job queue for the large dev.to community. Smaller Forem instances use the standard async path. The comment markers (`@sre:mstruve`) signal that this divergence is tracked by the SRE team and expected to be removed once a more scalable solution is in place.

## Key Members

- `starting_id` / `ending_id` — user ID range to scope the query, defaulting to 1–50,000,000, allowing callers to shard processing across workers.
- `email_digest_periodic` — the notification setting flag that gates whether a user receives digest emails.

## Scenarios

### Enqueue worker skips dispatch on dev.to

1. `Emails::EnqueueDigestWorker` is invoked by the Sidekiq scheduler.
2. The worker detects that the current Forem instance is dev.to.
3. The worker exits early without calling `EmailDigest.send_periodic_digest_email`.

### Enqueue worker triggers digest dispatch on non-dev.to instances

1. `Emails::EnqueueDigestWorker` is invoked by the Sidekiq scheduler.
2. The worker detects the instance is not dev.to.
3. The worker calls `EmailDigest.send_periodic_digest_email` with no arguments, using default ID range and all eligible users.

### Digest emails enqueued asynchronously for each eligible user

1. `EmailDigest` fetches registered users with `email_digest_periodic` enabled and a non-empty email address, within the specified ID range.
2. Users are processed in batches; for each user, `Emails::SendUserDigestWorker` is enqueued asynchronously via Sidekiq.

### Digest emails dispatched inline on dev.to

1. `EmailDigest` fetches eligible users as above.
2. For each user, `Emails::SendUserDigestWorker` is instantiated and its `perform` method is called directly (inline, synchronous) rather than enqueued.

## Failures / Exceptions

- If dispatching fails for an individual user, the `StandardError` is rescued, reported to Honeybadger, and processing continues with the next user in the batch.
