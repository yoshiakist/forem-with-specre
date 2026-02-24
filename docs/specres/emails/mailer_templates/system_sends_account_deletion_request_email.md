---
id: "01KJ72PVG4W2F3ADXJKS59C3S2"
name: "system_sends_account_deletion_request_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `app/views/mailers/notify_mailer/account_deletion_requested_email.html.erb`
- `app/views/mailers/notify_mailer/account_deletion_requested_email.text.erb`
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When a user requests deletion of their account, the system sends a transactional confirmation email to the user's registered address. The email contains a time-limited confirmation link (valid for 12 hours) that the user must follow to complete the deletion. Both an HTML and a plain-text version of the email are delivered. The subject line is localized and includes the community name resolved from the user's subforem context. The email body also includes the platform's contact address so the user can reach support if needed.

## Design Intent

Requiring a second confirmation step via a tokenized link prevents accidental or unauthorized account deletions. The 12-hour expiry window balances user convenience against the risk of a stale confirmation link being exploited. Sending both HTML and plain-text parts ensures deliverability across all email clients.

## Key Members

- `user` — the User record whose account is being deleted; supplies the recipient address and display name
- `token` — a short-lived secret string embedded in the confirmation URL; identifies the pending deletion request
- `@name` — the user's display name, rendered in the email greeting
- `@token` — the token passed to `user_confirm_destroy_url` to construct the confirmation link
- subject key `mailers.notify_mailer.deletion_requested` — I18n key used to build the localized subject line, interpolating `community` from `Settings::Community.community_name`

## Scenarios

### Sending the deletion request confirmation email

1. The system calls `NotifyMailer.with(user:, token:).account_deletion_requested_email`.
2. The mailer resolves the user's display name and the one-time token from the params.
3. The subject is built by looking up the I18n key `mailers.notify_mailer.deletion_requested`, interpolating the community name for the user's subforem context.
4. The email is addressed to the user's registered email address.
5. Both the HTML and plain-text parts are rendered from their respective templates.
6. The HTML template displays a personalized greeting, a clickable confirmation link pointing to `user_confirm_destroy_url(@token)`, and the platform's contact email address.
7. The plain-text template presents the same information without markup, with the confirmation URL written out in full.
8. The email is signed off with the community team name.

## Failures / Exceptions

- If the token has expired (older than 12 hours) and the user follows the link, the confirmation endpoint (outside this mailer's scope) rejects the request; the mailer itself does not validate expiry at send time.
- If `ForemInstance.contact_email` is blank, the contact paragraph renders an empty address; no error is raised by the mailer.
