---
id: "01KJ72G2KV3QBHWF11ZNJKHREH"
name: "system_sends_password_reset_instructions_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/devise_mailer.rb`
- `app/views/devise/mailer/reset_password_instructions.html.erb`
- `spec/mailers/devise_mailer_spec.rb` (Test)

## Functional Overview

When a user requests a password reset, the system sends a transactional email containing a secure, time-limited link to the `edit_password_url` endpoint with the user's reset token embedded. The email is delivered via `DeviseMailer`, which inherits Devise's default `reset_password_instructions` action without overriding it. Before the email is sent, two before-actions run: one sets the sender address to the community name and configured `from_email_address`, and another resolves the subforem context for the requesting user — so that the reset link domain reflects the user's associated subforem rather than the platform's global `app_domain`. Click tracking is explicitly disabled to prevent spam-filter false positives on security emails.

## Design Intent

The `reset_password_instructions` method is intentionally left un-overridden in `DeviseMailer`; Devise's default implementation is sufficient. Custom behavior is injected entirely through before-actions (`use_settings_general_values` and `setup_subforem_context`) and a bespoke HTML template, keeping the mailer class thin. Disabling Ahoy click tracking (`def save_ahoy_options; end`) is a deliberate trade-off: security-sensitive emails must not carry third-party tracking parameters that trigger spam filters, even at the cost of losing click analytics.

## Key Members

- `DeviseMailer#use_settings_general_values` — sets `Devise.mailer_sender` to `"<community_name> <from_email_address>"` and sets the default URL host to `Settings::General.app_domain`
- `DeviseMailer#setup_subforem_context` — resolves `@subforem_id` and `@subforem_domain` from the user's `onboarding_subforem_id`; overrides the URL host with the subforem domain when one is found
- `ForemInstance.reply_to_email_address` — used as the `reply_to` header default for all `DeviseMailer` emails
- `@resource` — the user record, provided by Devise; used in the template to render the user's email address
- `@token` — the password reset token, provided by Devise; embedded in the reset URL

## Scenarios

### Standard password reset (no subforem)

1. User requests a password reset on a platform with no subforem configuration.
2. `use_settings_general_values` sets the sender to `"<community_name> <from_email_address>"` and the URL host to `Settings::General.app_domain`.
3. `setup_subforem_context` finds no subforem for the user and leaves the URL host unchanged.
4. Devise's default `reset_password_instructions` action is called with the user record and a generated token.
5. The template renders a greeting with the user's email address, a plain-text explanation, and a "Change my password" link pointing to `edit_password_url` with the reset token.
6. The email is delivered with the community sender in `From`, the configured address in `Reply-To`, and the app domain in the reset link.
7. No Ahoy click-tracking parameters appear in the email body or links.

### Password reset for a user associated with a subforem

1. User with an `onboarding_subforem_id` requests a password reset.
2. `use_settings_general_values` sets the initial URL host to `Settings::General.app_domain`.
3. `setup_subforem_context` resolves the user's subforem domain from `Subforem.cached_id_to_domain_hash` and overrides `ActionMailer::Base.default_url_options[:host]` with that domain.
4. Devise's default action renders the email using the subforem domain in the reset password link.
5. The recipient receives a link that navigates them to the correct subforem, not the platform's default domain.

## Failures / Exceptions

- If the subforems table does not exist or raises a database error during `setup_subforem_context`, the error is rescued and the URL host falls back to `Settings::General.app_domain` or `ApplicationConfig["APP_DOMAIN"]`, ensuring the email is still delivered.
- If `Subforem.cached_id_to_domain_hash` does not contain the user's subforem ID, `determine_subforem_domain` falls back to `Subforem.cached_default_domain`, then to `Settings::General.app_domain`, then to `ApplicationConfig["APP_DOMAIN"]`.
- The `Deliverable` concern may suppress delivery entirely when SMTP settings are not configured; this is a cross-cutting concern handled outside this behavior.
