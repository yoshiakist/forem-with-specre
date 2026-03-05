---
id: "01KJ72JZVZK090J0RBBA6TGRSP"
name: "system_sends_unread_notifications_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb` (Source)
- `app/views/mailers/notify_mailer/unread_notifications_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/unread_notifications_email.text.erb` (Template)
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When a user has unread notifications, the system sends a digest email to that user's address summarizing how many unread notifications they have. The email subject line includes the unread count and the community name (resolved per-subforem). The HTML body renders a prominent call-to-action button linking directly to the notifications page, and the plain-text body provides an equivalent plain URL. Before sending, the mailer checks the per-address rate limit and silently aborts if the limit has been reached. An unsubscribe token scoped to `email_unread_notifications` is generated and made available to the templates.

## Design Intent

The email is intentionally minimal: it does not enumerate individual notifications, only the count. This keeps the email lightweight and avoids privacy-sensitive content leaking into inboxes while still providing a clear prompt to return to the platform. The rate-limit guard prevents repeated digest emails from being sent to the same address in a short window. The subforem-aware community name allows multi-tenant deployments to brand the subject line correctly.

## Key Members

- `@user` — the recipient; resolved from `params[:user]`
- `@unread_notifications_count` — integer count of the user's unread notifications at send time
- `@unsubscribe` — signed token for the `email_unread_notifications` preference; available to templates for an unsubscribe link
- Subject i18n key: `mailers.notify_mailer.unread_notifications` — interpolates `count` and `community`

## Scenarios

### Email is sent successfully

1. The caller provides a `user` param with a valid email address.
2. The rate-limit check passes (the address has not exceeded its send quota).
3. The mailer counts the user's unread notifications and generates an unsubscribe token.
4. The subject is built from the i18n key, embedding the unread count and the community name for the user's subforem.
5. The email is delivered to the user's address with the correct subject.
6. The HTML body contains a button linking to the notifications page; the plain-text body contains the equivalent URL.

### Subforem context affects subject and links

1. The mailer is invoked in a subforem context (e.g., a custom domain subforem).
2. `Settings::Community.community_name` returns the subforem's community name rather than the default.
3. The subject line reflects the subforem community name.
4. Links in the templates resolve to the subforem domain via `app_url`.

## Failures / Exceptions

- If the user's email address has exceeded the per-address rate limit (`RateLimitChecker#limit_by_email_recipient_address` returns truthy), the method returns early and no email is sent.
