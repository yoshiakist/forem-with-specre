---
id: "01KJ7408K5C6ZFPGTNP24020H9"
name: "system_sends_onboarding_drip_emails"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/workers/emails/drip_email_worker.rb`
- `spec/workers/emails/drip_email_worker_spec.rb` (Test)

## Functional Overview

A background Sidekiq worker, `Emails::DripEmailWorker`, sends timed onboarding emails to newly registered users by matching each user's registration timestamp against a series of day-based drip windows. When the feature flag `onboarding_drip_emails` is enabled, the worker iterates from day 1 up to the highest configured drip day, computes the corresponding 24-hour window for each day, queries users who registered in that window, and delivers a personalised `CustomMailer` email using an active template selected by the user's `onboarding_subforem_id`. Users who have unsubscribed from the newsletter or who received any email in the past 12 hours are silently skipped.

## Design Intent

Templates are resolved in two groups: the "default" group (users whose `onboarding_subforem_id` is `nil` or equals `Subforem.cached_default_id`) and custom groups (all other subforem IDs). This allows platform operators to maintain a single default drip sequence while independently customising sequences for specific subforems. Treating both `nil` and the cached default ID as equivalent prevents duplicate sequences when the default subforem ID is set.

## Key Members

- `drip_day` — integer day index (1-based); used to compute the 24-hour registration window and to select the matching email template
- `onboarding_subforem_id` — user attribute that determines which template variant is delivered (nil / default vs. custom subforem)
- `email_newsletter` — user notification setting; must be `true` for the email to be sent
- `EmailMessage.sent_at` — used to enforce a 12-hour cooldown between emails per user

## Scenarios

### Feature flag disabled — no emails sent

1. The worker is invoked.
2. The feature flag `onboarding_drip_emails` is disabled.
3. The worker exits immediately without querying users or sending any emails.

### No active drip email templates — no emails sent

1. The feature flag `onboarding_drip_emails` is enabled.
2. No `onboarding_drip` emails exist in the database, so the maximum `drip_day` is `nil`.
3. The worker exits immediately without sending any emails.

### Default template delivered to users registered on the expected day

1. The feature flag is enabled and at least one `onboarding_drip` email with `drip_day: N` exists.
2. The worker computes the 24-hour window for day N (from N×24+1 hours ago to N×24 hours ago).
3. It finds users who registered within that window and whose `onboarding_subforem_id` is `nil` or equals `Subforem.cached_default_id`.
4. For each eligible user who is subscribed and has not been emailed in the last 12 hours, it selects the lowest-ID active template in the default group for that drip day.
5. The email is delivered via `CustomMailer` with the template's subject and body.

### Custom template delivered to users in a specific subforem

1. A user registered in drip day N's window has a non-default `onboarding_subforem_id`.
2. The worker looks up an active `onboarding_drip` template matching that exact `onboarding_subforem_id` and `drip_day`.
3. If a matching template exists, the email is delivered with that template's subject and body.
4. If no matching custom template exists, the user is skipped for this drip day.

### Eligible user skipped due to unsubscribe or recent email

1. A user registered in drip day N's window has `email_newsletter` set to `false`, or has received an email within the past 12 hours.
2. The worker evaluates each guard condition per user before selecting a template.
3. The user is skipped without sending an email or logging an error.

## Failures / Exceptions

- If delivering an email raises a `StandardError`, the error is caught, logged to `Rails.logger.error` with the user ID and message, and processing continues with the remaining users. Individual delivery failures do not abort the overall job.
