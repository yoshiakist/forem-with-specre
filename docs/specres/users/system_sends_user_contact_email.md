---
id: "01KJ9JGXPSJEWB4J1HDKAJ71WD"
name: "system_sends_user_contact_email"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `app/views/mailers/notify_mailer/user_contact_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/user_contact_email.text.erb` (Template)
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When an administrator or system process needs to contact a specific user directly, the system composes and delivers an email to that user. The mailer action accepts a user ID, a subject line, and a body message as parameters, then looks up the user record to obtain their email address. It sends the message to that address with the provided subject. Both HTML and plain-text versions of the email are rendered, with the HTML variant applying paragraph formatting to the body and the plain-text variant delivering the raw body content unchanged.

## Key Members

- `user_id` — identifier used to look up the recipient user record
- `email_subject` — string passed directly as the email subject line
- `email_body` — string used as the full body content in both HTML and plain-text templates

## Scenarios

### System delivers a contact email to a user

1. The caller provides a user ID, a subject string, and a body string as parameters.
2. The system retrieves the user record matching the given user ID to determine the recipient's email address.
3. The system composes an email addressed to the user's email address, using the provided subject line.
4. The HTML version of the email renders the body with paragraph formatting applied.
5. The plain-text version of the email renders the body as-is, without any additional formatting.
6. The email is dispatched to the user's address.

### Email headers are correctly set

1. The system sets the `to` header to the resolved user's email address.
2. The system sets the `subject` header to the value supplied by the caller.
3. Standard mailer headers (e.g., `from`) are applied according to the shared mailer defaults.
