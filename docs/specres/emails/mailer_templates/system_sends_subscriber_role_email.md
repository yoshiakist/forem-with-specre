---
id: "01KJ72WHJG3KGKQRANX95KQTSX"
name: "system_sends_subscriber_role_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `spec/mailers/notify_mailer_spec.rb` (Test)
- `app/views/mailers/notify_mailer/base_subscriber_role_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/base_subscriber_role_text.html.erb` (Template)

## Functional Overview

When a user is granted the base subscriber role (DEV++), the system sends a congratulatory email confirming their subscription. The email is addressed to the user's registered email address and carries a community-aware subject line built from the current community name. Both an HTML and a plain-text variant are rendered. The HTML body greets the user by name, links to the DEV++ hub, and includes an early-bird message. The plain-text body carries equivalent content in a link-safe format.

## Design Intent

The email is delivered through the standard `NotifyMailer` pattern and uses `I18n.t` for the subject so that subforem-aware community names are automatically substituted, making the email contextually correct regardless of which subforem the user belongs to.

## Key Members

- `@user` — the recipient; supplies `name` and `email`
- `subject` — resolved via `I18n.t("mailers.notify_mailer.base_subscriber", community: ...)`, e.g. "Congrats! You're now subscribed to DEV++"
- `@subforem_id` — used to resolve the community name for the subject line in subforem contexts

## Scenarios

### Standard delivery

1. A user is granted the base subscriber (DEV++) role.
2. The system calls `NotifyMailer.with(user: user).base_subscriber_role_email`.
3. The mailer sets `@user` from params and resolves the subject using the community name for the current subforem.
4. An email is sent to `@user.email` with the resolved subject.
5. The HTML template greets the user by name and provides a link to the DEV++ hub along with an early-bird notice.
6. The plain-text template delivers equivalent greeting and hub URL content.

### Subforem context

1. When the mailer runs within a subforem context, `@subforem_id` is set.
2. `Settings::Community.community_name(subforem_id: @subforem_id)` returns the subforem-specific community name.
3. The subject line reflects the subforem community rather than the default community name.
4. Links in the rendered templates use the subforem's domain.

## Failures / Exceptions

- If `@user.email` is blank or invalid, delivery will fail at the mail transport layer; the mailer itself does not validate the address.
- If the `I18n` key `mailers.notify_mailer.base_subscriber` is missing for a given locale, Rails falls back to the default locale subject.
