---
id: "01KHZ3SPSJ823DQWH7K6DW74FF"
name: "admin_can_configure_authentication_providers"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/settings/authentications_controller.rb`
- `app/models/settings/authentication.rb`
- `app/lib/constants/settings/authentication.rb`
- `app/services/settings/authentication/upsert.rb`
- `app/views/admin/settings/forms/_authentication.html.erb` (Template)
- `app/views/admin/settings/forms/authentication/_auth_provider_settings.html.erb` (Template)
- `app/views/admin/settings/forms/authentication/_apple_auth_provider_settings.html.erb` (Template)
- `spec/models/settings/authentication_spec.rb` (Test)
- `spec/models/settings/authentication_integration_spec.rb` (Test)
- `spec/services/settings/authentication/upsert_spec.rb` (Test)

## Functional Overview

A super-admin can configure how users authenticate with the Forem instance. This includes enabling or disabling OAuth providers (GitHub, Google, Facebook, Twitter, Apple, Forem), toggling email/password registration, restricting registration by email domain (block-list and allow-list), requiring CAPTCHA for email registration, and setting the default status for newly registered users. The authentication upsert service validates that provider credentials are complete before enabling a provider, and prevents disabling email/password login when fewer than two OAuth providers are enabled.

## Key Members

- `auth_providers_to_enable` — list of provider names to activate; drives the enable/disable toggle logic in the upsert service
- `new_user_status` — enum (`"good_standing"` or `"limited"`) controlling initial trust level for new registrations
- `allowed_registration_email_domains` / `blocked_registration_email_domains` — arrays controlling domain-level registration restrictions

## Scenarios

### Admin enables an OAuth provider

1. Admin enters the client key and secret for a provider (e.g., GitHub)
2. Admin adds the provider name to the `auth_providers_to_enable` list
3. `Settings::Authentication::Upsert` verifies the provider is in `Authentication::Providers.available`
4. Service confirms both key and secret are present
5. Provider is enabled and credentials are persisted

### Admin enables Apple authentication

1. Admin enters the four required Apple credentials: client ID, key ID, PEM content, and team ID
2. System synthesizes these into `apple_key` and `apple_secret` (returning `"present"` when all four are set)
3. Apple provider is enabled

### Admin toggles email/password registration

1. Admin enables or disables the `allow_email_password_registration` setting
2. If disabling email login and fewer than two OAuth providers are enabled, upsert rejects the change with an error
3. Admin can optionally require CAPTCHA by setting `recaptcha_site_key` and `recaptcha_secret_key`

### Admin restricts registration by email domain

1. Admin adds domains to the `blocked_registration_email_domains` list
2. System blocks registration attempts from those domains, including subdomains (e.g., blocking `example.com` also blocks `sub.example.com`)
3. Alternatively, admin sets `allowed_registration_email_domains` to restrict registration to only listed domains
4. Domain blocking also integrates with the `BlockedEmailDomain` model for persistent domain blocks
5. `acceptable_domain?` checks both settings-based and model-based blocks, with suffix-aware matching

### Admin sets new user default status

1. Admin selects `"good_standing"` or `"limited"` for `new_user_status`
2. When set to `"limited"`, `limit_new_users?` returns true
3. Newly registered users receive the configured status, which affects their initial permissions
