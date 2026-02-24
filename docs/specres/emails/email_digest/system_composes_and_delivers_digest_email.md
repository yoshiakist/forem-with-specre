---
id: "01KJ71J0WWYVQ1PD8KP1MBS1W0"
name: "system_composes_and_delivers_digest_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/workers/emails/send_user_digest_worker.rb`
- `app/mailers/digest_mailer.rb`
- `app/views/mailers/digest_mailer/digest_email.html.erb` (Template)
- `spec/workers/emails/send_user_digest_worker_spec.rb` (Test)
- `spec/mailers/digest_mailer_spec.rb` (Test)
- `spec/mailers/previews/digest_mailer_preview.rb` (Test)

## Functional Overview

When the periodic digest job runs for a user, the system collects a set of recommended articles and two billboard slots (a primary and a paired or fallback secondary), optionally generates an AI-powered smart summary for recently active users, then renders and delivers a digest email via `DigestMailer`. The email subject line adapts to the platform (DEV vs. generic Forem) and whether the user follows any subforems. Billboard impression events are recorded synchronously after delivery. Errors during delivery or event recording are reported to Honeybadger without re-raising, so a single failure does not block the job queue.

## Design Intent

The worker separates article collection (`EmailDigestArticleCollector`) from email composition, keeping the mailer focused on rendering. The paired billboard mechanism allows ad operations to guarantee that a specific second billboard always accompanies a given first billboard, falling back to an independent selection otherwise. The AI smart summary (see specre `01KJ6T999JZFEAT9S2K18TXENM` in the `ai_features` domain) is conditionally generated only for users active within the past three days, limiting AI compute to users most likely to engage. Errors are swallowed at the job boundary rather than retried after the delivery attempt, because a partially-sent email cannot be unsent.

## Key Members

- `force_send` — boolean flag passed to the worker; bypasses the user's `email_digest_periodic` notification preference and the article-collection freshness gate when `true`
- `first_billboard` / `second_billboard` — ad slots rendered inside the email; `second_billboard` is resolved as the paired partner of `first_billboard` when one exists, otherwise selected independently
- `smart_summary` — AI-generated overview text, present only when `user.last_presence_at` is within the past three days
- `@unsubscribe` — one-click unsubscribe token embedded in the mailer for the `email_digest_periodic` preference

## Scenarios

### Delivering a standard digest email

1. The Sidekiq job receives a `user_id` and an optional `force_send` flag (default `false`).
2. The system loads the user and aborts if the user is not registered.
3. Unless `force_send` is `true`, the system checks the user's `email_digest_periodic` notification setting and aborts if it is disabled.
4. The system fetches the list of articles to send; if none are available it aborts.
5. The system resolves two billboard slots using the user's followed tag names as targeting context, preferring a pre-paired second billboard when one exists.
6. The system generates an AI smart summary if the user was active within the past three days; otherwise `smart_summary` is `nil`.
7. `DigestMailer` renders the digest email with the articles, billboards, and smart summary, then delivers it immediately.
8. If any billboards were shown, the system records a billboard impression event for each one inside a synchronous-commit-off transaction.

### Skipping delivery for ineligible users

1. The job receives a `user_id` for a user who is unregistered, has the digest notification disabled, or has no collectible articles.
2. The system exits early without sending an email or recording any billboard events.

### Bypassing notification preference with force_send

1. The job receives `user_id` and `force_send: true`.
2. The system skips the `email_digest_periodic` preference check and any freshness gate inside the article collector.
3. Delivery proceeds normally if articles are available.

### Composing the email subject line

1. `DigestMailer` builds the subject by calling `generate_title`.
2. On DEV (`ForemInstance.dev_to?`), if the user follows any subforems, the subject is formatted as `"<first article title> | Forem Digest"`; otherwise it uses `"<first article title> | DEV Digest"`.
3. On a generic Forem instance the subject is the bare first article title.
4. If SendGrid is enabled, the mailer adds an `X-SMTPAPI` header categorising the message as `"Digest Email"`.

### Handling delivery errors gracefully

1. Any `StandardError` raised during email delivery or billboard event creation is caught by the worker.
2. The worker attaches the `user_id` and article IDs as Honeybadger context, then notifies Honeybadger of the exception.
3. The job completes without re-raising, preventing unnecessary retries for non-transient failures.

## Failures / Exceptions

- If `DigestMailer#deliver_now` or billboard event creation raises a `StandardError`, the worker rescues it, sends a report to Honeybadger with user and article context, and exits cleanly without retrying the delivery.
- Billboard events are written with `synchronous_commit` turned off, so event persistence failures do not block or roll back email delivery.
