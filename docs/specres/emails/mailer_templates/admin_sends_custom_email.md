---
id: "01KJ7297CDCGQ36QFHNA8BR6XJ"
name: "admin_sends_custom_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/custom_mailer.rb`
- `app/views/mailers/custom_mailer/custom_email.html.erb` (Template)
- `spec/mailers/custom_mailer_spec.rb` (Test)
- `spec/mailers/previews/custom_mailer_preview.rb` (Test)

## Functional Overview

`CustomMailer` delivers one-off or campaign emails to individual users on behalf of the platform admin. The single `custom_email` action resolves merge tags in both the subject and body, generates an unsubscribe token, determines the sender display name from either an explicit `from_name` param or by looking it up from the associated `Email` record's type, and sends the message. When SendGrid is the active mail provider, the action also injects an `X-SMTPAPI` JSON header that categorises the send and attaches a `mailing_id` unique argument for tracking. Delivery history is recorded via `has_history`, keyed on `email_id`.

## Key Members

- `params[:user]` — the recipient; must respond to `email` and `name`
- `params[:content]` — raw HTML body; `*|name|*` merge tags are replaced before send
- `params[:subject]` — email subject line; merge tags are also replaced
- `params[:email_id]` — ID of the `Email` record; used for history tracking and fallback sender-name lookup
- `params[:from_name]` — optional explicit sender display name; overrides the `Email` record lookup when present
- `params[:type_of]` — optional label for the SendGrid category (defaults to `"Custom"`)

## Scenarios

### Merge tags are replaced in content and subject

1. A caller invokes `CustomMailer.with(user:, content:, subject:).custom_email`.
2. The mailer replaces every `*|name|*` placeholder in `content` and `subject` with the user's actual name.
3. The rendered email is addressed to the user's email address and carries the resolved subject line.
4. The body includes the user's unsubscribe token so the template can render the unsubscribe link.

### SendGrid header is set when SendGrid is enabled

1. Before sending, the mailer checks whether SendGrid is active for the current Forem instance.
2. When enabled, it builds a JSON object containing a `category` (e.g. `"Custom Email"`) and a `unique_args` map with a `mailing_id` of the form `email-instance-<email_id>`.
3. This JSON string is attached as the `X-SMTPAPI` request header so SendGrid can route and track the send.

### No SendGrid header when SendGrid is disabled

1. When SendGrid is not active, the mailer skips the header injection step entirely.
2. The email is sent without an `X-SMTPAPI` header.

### Delivery is tracked against the Email record

1. When `email_id` is supplied, `has_history` captures the `email_id` as an extra attribute on the resulting `EmailMessage` record.
2. After delivery, the associated `Email` record shows one new `EmailMessage` in its history.

### Sender display name is resolved from from_name or Email type

1. If `from_name` is provided in `params`, the mailer uses it directly as the display name without querying the database.
2. If `from_name` is absent or `nil`, the mailer loads the `Email` record by `email_id` and reads its `default_from_name_based_on_type`.
3. For `onboarding_drip` emails the display name becomes `"<Community> Onboarding"`; for `newsletter` it becomes `"<Community> Newsletter"`; for `one_off` it falls back to just the community name.
4. The resolved display name is combined with the platform's configured reply-to address to form the `From` header.
