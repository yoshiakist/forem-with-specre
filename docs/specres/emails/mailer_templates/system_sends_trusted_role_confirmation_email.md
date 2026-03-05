---
id: "01KJ72SXAQ2WNCG8H8P8PXR5E0"
name: "system_sends_trusted_role_confirmation_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `app/views/mailers/notify_mailer/trusted_role_email.html.erb`
- `app/views/mailers/notify_mailer/trusted_role_email.text.erb`
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When a user is granted the "trusted" role, the system sends a confirmation email congratulating them and describing the new capabilities they have gained. The email is addressed to the user personally, names the community (resolved per-subforem when applicable), and lists the three new moderation abilities: emoji-based content ranking, post experience-level rating, and flagging problematic content to admins. If the community has a "trusted-member" page, the email links to it as a guide. Both HTML and plain-text variants of the email body are rendered.

## Design Intent

The subject line and community name are resolved through `Settings::Community.community_name` with an optional `subforem_id`, allowing a single mailer method to serve both the global community and any subforem that has its own branding. This keeps subforem-aware personalisation consistent with the pattern used throughout `NotifyMailer`.

## Key Members

- `params[:user]` — the `User` record receiving the promotion; their `email` and `name` are used in the message
- `Settings::Community.community_name(subforem_id:)` — returns the community display name, subforem-specific when a subforem context is active
- `Page.find_by(slug: "trusted-member")` — conditional check; the Trusted Member Guide link is only rendered when this page exists
- Subject template key: `mailers.notify_mailer.trusted` — interpolates `community` to produce `Congrats! You're now a "trusted" user on <community>!`

## Scenarios

### Standard trusted-role notification

1. A user is elevated to the "trusted" role in the system.
2. `NotifyMailer.with(user: user).trusted_role_email` is called.
3. The mailer resolves the community name for the default (global) subforem.
4. An email is sent to the user's address with the subject `Congrats! You're now a "trusted" user on <community>!`.
5. The email body greets the user by name and announces that Trusted Member permissions have been granted.
6. The body lists the three new abilities: emoji content ranking, experience-level rating, and flagging content to admins.
7. If a page with slug `trusted-member` exists, a link to the Trusted Member Guide is included.
8. Both an HTML part and a plain-text part are delivered.

### Subforem-specific trusted-role notification

1. The receiving user was onboarded under a specific subforem (e.g., `trusted.example.com`).
2. The mailer resolves `Settings::Community.community_name` with the subforem's ID, returning the subforem's display name.
3. The email subject uses the subforem community name: `Congrats! You're now a "trusted" user on <subforem community name>!`.
4. Any links in the email body use the subforem's domain rather than the global domain.

## Failures / Exceptions

- No rate-limiting guard is applied in `trusted_role_email` (unlike several other `NotifyMailer` methods). If the user's email address is blank or invalid the standard mail delivery layer will raise an error at send time.
- If the `trusted-member` page does not exist, the guide link section is silently omitted from both HTML and text templates.
