---
id: "01KJ72PNMHN5CAC6ANK4VBMJJW"
name: "admin_sends_contact_email_to_user"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb` (NotifyMailer#user_contact_email)
- `app/views/mailers/notify_mailer/user_contact_email.html.erb` (HTML template)
- `app/views/mailers/notify_mailer/user_contact_email.text.erb` (Text template)
- `spec/mailers/notify_mailer_spec.rb` (Test, #user_contact_email section)

## Functional Overview

An admin can send a free-form contact email directly to any user. The mailer looks up the target user by their ID, uses the caller-supplied subject and body, and addresses the message to the user's email address. The HTML template renders the body through `simple_format` to preserve paragraph structure, while the plain-text template renders the body verbatim. No unsubscribe token is generated and no rate-limiting is applied; this path is reserved for intentional, admin-initiated contact.

## Design Intent

This action is distinct from system-notification emails (which carry unsubscribe tokens and are rate-limited) because it represents a deliberate, one-off administrative message rather than an automated notification. Keeping subject and body as caller-supplied parameters gives the admin full control over the message without requiring code changes for each use case.

## Key Members

- `params[:user_id]` — ID of the recipient user; the mailer resolves the full record and its email address from this value
- `params[:email_subject]` — Subject line passed verbatim to the mail header
- `params[:email_body]` — Body text rendered in both HTML and plain-text templates
- `@user` — Resolved User record; its `.email` attribute is used as the To address
- `@email_body` — Instance variable exposed to both view templates

## Scenarios

### Admin sends a contact email to a user

1. The caller invokes `NotifyMailer` with `user_id`, `email_subject`, and `email_body` parameters and requests `user_contact_email`.
2. The mailer fetches the User record matching `user_id`.
3. The mailer composes an outbound email addressed to the user's email, using the supplied subject.
4. The HTML part renders the body through `simple_format`, wrapping it in paragraph tags.
5. The plain-text part renders the body as-is.
6. The email is delivered to the user.

## Failures / Exceptions

- If no user exists for the given `user_id`, `User.find` raises `ActiveRecord::RecordNotFound` and the email is not sent.
