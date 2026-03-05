---
id: "01KJBKJ3R73H0D2V7BGCMMRQDM"
name: "user_can_sign_up_or_log_in_with_forem"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/authentication/providers/forem.rb`
- `app/views/shared/authentication/_initial_account_wizard.html.erb` (Template)
- `app/views/shared/authentication/_forem_creator_signup.html.erb` (Template)
- `spec/services/authentication/providers/forem_spec.rb` (Test)
- `spec/system/authentication/user_logs_in_with_forem_spec.rb` (Test)
- `spec/system/authentication/omniauth_redirect_uri_spec.rb` (Test)
- `spec/system/authentication/creator_config_edit_spec.rb` (Test)

## Functional Overview

Users can sign up or log in to a Forem community using OAuth credentials from another Forem instance (e.g., account.forem.com). The `Authentication::Providers::Forem` class maps the OmniAuth payload to user attributes — email, display name, remote profile image, and Forem username — and passes no-op payload cleanup since the Forem provider does not contain sensitive fields to redact. For brand-new communities that have no owner yet, the initial account wizard guides the first user through setup steps before presenting an email-based registration form. The creator signup view collects name, username, email, password, and optionally a Forem owner secret when the instance requires one.

## Design Intent

The Forem provider is designed for the "creator OAuth" flow: a community creator authenticates via a trusted Forem identity provider rather than a third-party service. This distinguishes subscriber sign-ins (any available provider) from creator/owner bootstrapping (Forem-specific). The `forem_username` attribute on the user is populated only by this provider, enabling cross-instance identity linking. The `FOREM_OAUTH_URL` config allows self-hosted deployments to point to their own Forem identity provider instead of account.forem.com.

## Scenarios

### New user signs up via Forem OAuth

1. User visits the sign-up page and clicks "Continue with Forem".
2. System redirects to the Forem OAuth provider (account.forem.com or configured `FOREM_OAUTH_URL`).
3. User authorizes the application on the provider.
4. System receives the OmniAuth callback, maps email, name, remote profile image URL, and Forem username from the payload.
5. A new user account is created, a remember token is set, and the user is redirected to onboarding.

### New user withholds email address

1. User authorizes via Forem OAuth but does not share their email with the application.
2. System still creates the account using the remaining attributes (name, Forem username, profile image).
3. User is redirected to onboarding as normal.

### Existing user logs in via Forem OAuth

1. User visits the sign-up/sign-in page and clicks "Continue with Forem".
2. System receives the OmniAuth callback and matches the identity to an existing user record.
3. User is logged in and redirected to the home page with `?signin=true`.

### Username collision on new signup

1. The Forem username derived from the OAuth payload already belongs to another user on this community.
2. System creates the new account with a temporary username that includes the original as a base.
3. User is redirected to onboarding where they can choose a permanent username.

### First-time community setup (initial account wizard)

1. A new Forem instance has no owner yet.
2. The initial account wizard view is displayed, presenting setup steps and an email registration form.
3. The community creator completes the wizard to establish the first owner account.

### Creator signs up via creator signup form

1. A user accesses the creator signup page.
2. The form collects name (with auto-suggested username hint), username, email, and password.
3. If the instance requires a Forem owner secret, an additional secret field is shown (or pre-filled from query params).
4. On successful submission, the creator account is registered.

## Failures / Exceptions

- **Invalid OAuth credentials**: OmniAuth callback error is raised; no user is created, and the failure is reported to Datadog via `ForemStatsClient`. The user is redirected to the sign-in page.
- **Validation failure** (e.g., name exceeding 100 characters): The user record is not saved; the error is reported to Honeybadger, and the user is redirected back to the registration page.
- **Invite-only mode**: When the community is in invitation-only mode, the "Continue with Forem" option is not presented on the sign-up page.
