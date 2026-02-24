---
id: "01KJ758K1CA5TWC5FHEKJZ52BT"
name: "admin_can_create_and_deliver_custom_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/email.rb`
- `app/controllers/admin/emails_controller.rb`
- `app/mailers/custom_mailer.rb`
- `app/validators/email_safe_html_validator.rb`
- `app/workers/emails/batch_custom_send_worker.rb`
- `app/workers/emails/enqueue_custom_batch_send_worker.rb`
- `app/views/admin/emails/index.html.erb` (Template)
- `app/views/admin/emails/show.html.erb` (Template)
- `app/views/admin/emails/new.html.erb` (Template)
- `app/views/admin/emails/edit.html.erb` (Template)
- `app/views/admin/emails/_form.html.erb` (Template)
- `app/views/mailers/custom_mailer/custom_email.html.erb` (Template)
- `spec/models/email_spec.rb` (Test)
- `spec/requests/admin/emails_spec.rb` (Test)
- `spec/validators/email_safe_html_validator_spec.rb` (Test)
- `spec/workers/emails/batch_custom_send_worker_spec.rb` (Test)
- `spec/workers/emails/enqueue_custom_batch_send_worker_spec.rb` (Test)
- `spec/factories/emails.rb` (Test)
- `spec/models/user_email_eligible_spec.rb` (Test)

## Functional Overview

Admins can compose, manage, and deliver custom emails (one-off, newsletter, or onboarding drip) through an admin interface backed by full CRUD operations. Each email record carries a subject, HTML body, type, status (`draft`, `active`, `delivered`), and an optional audience target — either an `AudienceSegment` or a custom `UserQuery`. When an email is activated (status changed to `active`), an `after_commit` callback automatically enqueues `EnqueueCustomBatchSendWorker`, which splits eligible recipients into batches and dispatches `BatchCustomSendWorker` jobs. Each batch job resolves users, skips duplicates that have already received a non-test delivery for the same email record, and delivers via `CustomMailer#custom_email`, which applies merge tags (`*|name|*`, `*|username|*`, `*|email|*`), generates per-user unsubscribe tokens, and optionally sets SendGrid tracking categories. Admins can also trigger a test delivery from the edit form by supplying a comma-separated list of email addresses; test sends bypass the duplicate-check guard. HTML body content is validated by `EmailSafeHtmlValidator`, which rejects JavaScript, external stylesheets, and content that is stripped more than 50% by the safe-list sanitizer.

## Design Intent

Audience targeting is decoupled through two optional associations: `AudienceSegment` for pre-defined groups and `UserQuery` for ad-hoc SQL-defined sets. This lets operators reuse existing segments without duplicating query logic. The deduplication guard in `BatchCustomSendWorker` (checking `ahoy_messages` for a prior non-test delivery) prevents accidental re-sends if a job is retried or the worker is called multiple times. The `[TEST]` subject prefix is the contract that distinguishes test deliveries from production ones so test sends do not block future live deliveries. A transaction-scoped `statement_timeout` in `EnqueueCustomBatchSendWorker` protects the database from long-running `UserQuery` executions.

## Key Members

- `Email#type_of` — enum: `one_off`, `newsletter`, `onboarding_drip`. Onboarding drip emails are excluded from the activation-triggered delivery path.
- `Email#status` — enum: `draft`, `active`, `delivered`. Transitioning to `active` triggers delivery; status is immediately updated to `delivered` afterwards.
- `Email#test_email_addresses` — transient (attr_accessor) comma-separated list used to trigger a test send without changing the record's status.
- `EnqueueCustomBatchSendWorker::BATCH_SIZE` — 1000 in production, 10 in other environments.
- `BatchCustomSendWorker` — throttled to a configurable concurrency limit (default 5) via `EMAIL_BATCH_CONCURRENCY_LIMIT`.

## Scenarios

### Admin creates a draft email

1. An admin navigates to the new email form (`/admin/emails/new`).
2. The form presents fields for subject, body, type, status, and an optional user query selector loaded from active `UserQuery` records.
3. The admin fills in a subject and body, selects `draft` status, and submits.
4. The system validates presence of subject and body, and that the body contains only email-safe HTML (no scripts, no external stylesheets).
5. On success, the record is saved with status `draft`, no delivery is triggered, and the admin is redirected to the show page with a "drafted" confirmation.
6. On failure, the form is re-rendered with inline validation errors.

### Admin activates an email to trigger bulk delivery

1. The admin edits an existing draft email and changes its status to `active`.
2. On save, the `after_commit` callback detects the status change and calls `EnqueueCustomBatchSendWorker#perform_async` with the email's ID.
3. The email record's status is immediately updated to `delivered` to prevent repeated enqueueing.
4. `EnqueueCustomBatchSendWorker` opens a database transaction with a scoped statement timeout, resolves the target audience (via `UserQuery` with custom SQL or via `AudienceSegment`/default scope), and splits eligible recipients into batches.
5. Each batch is handed off to `BatchCustomSendWorker` as a separate background job.
6. `BatchCustomSendWorker` loads users in a single query, skips any user who already received a non-test delivery for this email, and delivers via `CustomMailer#custom_email` for each remaining user.
7. `CustomMailer` applies merge tags to subject and body, generates an unsubscribe token, sets SendGrid category headers when SendGrid is enabled, and sends the email.

### Admin sends a test delivery before activating

1. From the email show or edit page, the admin enters comma-separated email addresses into the test delivery field and submits.
2. The controller detects the `test_email_addresses` parameter and calls `deliver_to_test_emails` rather than updating the record.
3. The system looks up users whose emails match the provided addresses and enqueues a `BatchCustomSendWorker` job with the subject prefixed by `[TEST] `.
4. The test send bypasses the duplicate-check guard, so it can be run multiple times without blocking a future live delivery.
5. The admin is redirected to the show page with a confirmation message listing the target addresses.

### Audience is filtered to email-eligible users only

1. Before any batch is enqueued, the worker applies the `User.email_eligible` scope to the candidate set.
2. A user is eligible only when they are registered, have a non-blank email address, have `email_newsletter` enabled in their notification settings, and hold neither the `suspended` nor `spam` role.
3. Users failing any criterion are excluded from all batches regardless of the audience target.

## Failures / Exceptions

- If the email body or subject is blank, `ActiveRecord` validation halts the save and returns errors to the form.
- If the body contains `<script>` tags, `javascript:` URIs, inline event handlers, external `<link>`/`<style>` tags, or `@import` directives, `EmailSafeHtmlValidator` adds an error and the save is rejected.
- If the body is long and sanitization strips more than 50% of its content, the validator warns that unsupported HTML elements are present.
- If a user ID in a batch does not exist in the database, the worker silently skips it.
- If `CustomMailer` raises a `StandardError` for a particular user, the error is logged and the worker continues with the remaining users in the batch.
- Onboarding drip emails are excluded from the activation-triggered delivery path; `deliver_to_users` returns early if `type_of == "onboarding_drip"`.
- If the email record cannot be found inside `EnqueueCustomBatchSendWorker`, the job returns early without enqueueing any batches.
