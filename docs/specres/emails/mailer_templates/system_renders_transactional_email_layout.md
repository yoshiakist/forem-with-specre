---
id: "01KJ72941YA33EA9WDJ7TVJA6P"
name: "system_renders_transactional_email_layout"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/application_mailer.rb`
- `app/mailers/concerns/deliverable.rb`
- `spec/mailers/application_mailer_spec.rb` (Test)
- `spec/mailers/shared_examples/renders_proper_email_headers.rb` (Test)
- `app/views/layouts/mailer.html.erb` (Template)
- `app/views/layouts/mailer.text.erb` (Template)
- `app/views/mailers/notify_mailer/_email_header.html.erb` (Template)

## Functional Overview

`ApplicationMailer` serves as the base class for all transactional emails in the application. It applies the "mailer" layout, configures the `from` address and `reply_to` dynamically using subforem-aware settings, and establishes SMTP delivery behavior through the `Deliverable` concern. Before each email action, it resolves the recipient user's subforem context to set the correct community name, domain, and URL host. The `Deliverable` concern gates delivery based on whether SMTP is enabled at runtime and merges the active SMTP credentials into every outgoing message. The HTML layout wraps the email body in a styled table, conditionally appends a magic-link sign-in prompt for users with no recent page views, renders an optional custom footer, and always includes unsubscribe and notification-settings links. The plain-text layout strips HTML tags and yields the body. The notify-mailer email header partial displays the community logo and the recipient's avatar at the top of each notification email.

## Design Intent

Subforem context is resolved in a `before_action` rather than per-mailer so that all child mailers automatically inherit the correct community name, domain, and URL host without each mailer needing to duplicate that logic. SMTP delivery control is likewise centralised in the `Deliverable` concern so that a single feature flag (`ForemInstance.smtp_enabled?`) governs whether any email is actually sent, preventing accidental delivery in environments without SMTP configured.

## Key Members

- `@subforem_id` — ID of the subforem resolved for the current recipient; used to scope community-name and domain lookups.
- `@subforem_domain` — Domain string set as `ActionMailer::Base.default_url_options[:host]` for URL generation within the email.
- `@unsubscribe` — Token set by child mailers; when present the layout renders a one-click unsubscribe link alongside the notification-settings link.
- `@user` — Recipient user object; the layout uses it to render the magic-link prompt and the signed-up-with footer line.

## Scenarios

### SMTP delivery is gated by the feature flag

1. Before each mailer action runs, the system checks whether SMTP is enabled via `ForemInstance.smtp_enabled?`.
2. `perform_deliveries` is set to `true` if SMTP is enabled, or `false` if it is not.
3. After the action completes, the current `Settings::SMTP` credentials are merged into the delivery method settings so the correct mail server is used.

### Subforem context is resolved from the recipient user

1. Before building the email, the system looks up the recipient user from the mailer parameters.
2. The user's `onboarding_subforem_id` is used to resolve the subforem ID and its associated domain.
3. If the user has no subforem ID, or the ID is not found in the cached domain map, the system falls back to the default subforem domain.
4. If no subforems exist, the system falls back to `Settings::General.app_domain`.
5. The resolved domain is set as the URL host for all links generated in the email.

### From address is built with subforem community name

1. When composing a `from` address, the system reads the community name scoped to `@subforem_id`.
2. If a topic string is provided (e.g., "Digest"), it is appended to the community name.
3. The resulting display name is combined with `ForemInstance.from_email_address` to form the full `from` header.
4. The `reply_to` header is set to `ForemInstance.reply_to_email_address`.

### HTML layout conditionally shows magic-link prompt

1. When the HTML layout renders, it checks whether `@user` is present and whether the action is not a magic-link email.
2. If the user's most recent page view is older than four weeks (or the user has no page views), the layout inserts a "Not signed-in on this device?" prompt with a magic-link sign-in button.
3. If the user has a recent page view, the prompt is omitted.
4. If a custom email footer is configured, it is rendered after the magic-link section.
5. An unsubscribe link (when `@unsubscribe` is set) or a notification-settings link is always rendered at the bottom.

### Notify-mailer email header partial renders branding and avatar

1. The partial renders a two-column header row: the community logo or name on the left, and the recipient's profile avatar on the right.
2. The logo links to the community root URL; the avatar links to the recipient's profile.
3. If no resized logo is configured, the community name is displayed as text instead.

## Failures / Exceptions

- If a database error occurs during subforem context setup (e.g., `ActiveRecord::StatementInvalid` or `ActiveRecord::NoDatabaseError`), the error is logged as a warning, `@subforem_id` is set to `nil`, and the domain falls back to `Settings::General.app_domain` or the `APP_DOMAIN` environment variable.
- In the development environment, port 3000 is appended to the resolved domain for local URL generation.
