---
id: "01KJBKE1C16S97KD8TGGV2RBK0"
name: "user_can_sign_up_or_log_in_with_apple"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/authentication/providers/apple.rb`
- `spec/system/authentication/user_logs_in_with_apple_spec.rb` (Test)

## Functional Overview

When Apple Sign-In is enabled on the platform, a visitor can authenticate via Apple ID using the OmniAuth Apple strategy. On first sign-in, Apple provides the user's email address and, optionally, their first and last name; on subsequent sign-ins Apple sends nil for those fields. The Apple provider maps this payload to Forem user attributes: it constructs a deterministic `apple_username` from name components hashed with a SHA-512 digest of the email to avoid collisions, and generates a profile image. For existing users returning after the first sign-in, only the username is conditionally updated (and only when Apple actually provides a name), leaving all other attributes unchanged.

## Design Intent

Apple's OAuth flow has two constraints that differ from other providers: (1) the user's email and name are only disclosed on the very first authorization — all subsequent logins send nil for those fields; and (2) Apple does not supply a `nickname` field, so a synthetic username must be derived from whatever name data is available. The `user_nickname` method hashes the email with SHA-512 as a suffix to guarantee a stable, collision-resistant identifier across logins even when names are absent. The `existing_user_data` method deliberately skips updating username when `first_name` is nil, so that re-authorizations after Apple revokes access do not overwrite a user's established username with a blank value.

## Scenarios

### New user signs up with Apple for the first time

1. A visitor who has never used the platform clicks "Continue with Apple" on the sign-up page.
2. Apple provides their email address and first/last name in the OAuth payload.
3. The system creates a new user account, assigns an `apple_username` derived from the name components and a hashed email suffix, and generates a profile image.
4. The user is redirected to the onboarding flow and a remember token is set.

### New user signs up when their derived username is already taken

1. A visitor clicks "Continue with Apple" and Apple provides a name that maps to an `apple_username` already used by another account.
2. The system creates the new user with a temporary username that still incorporates the existing username as a prefix.
3. The user is redirected to the onboarding flow.

### Existing user logs in with Apple on a subsequent visit

1. A user who previously authorized with Apple returns and clicks "Continue with Apple".
2. Apple sends nil for first name, last name, and email (post-first-authorization behavior).
3. The system matches the Apple identity to the existing user account and logs them in without changing any user attributes.
4. The user is redirected to the home feed.

### Authentication fails due to invalid credentials or OAuth error

1. The Apple OAuth callback returns an error (e.g., `CallbackError`, `OAuth::Unauthorized`, or no error object).
2. No user account is created or modified.
3. The system increments a Datadog metric (`omniauth.failure`) with the provider name and error details.

## Failures / Exceptions

- If user data from Apple fails Forem model validation (e.g., a name exceeding 100 characters), the user is not created and the system redirects back to the registration page. Honeybadger is notified of the error.
- If the Apple OAuth callback returns an error for any reason, no user record is persisted and Datadog is notified via `ForemStatsClient.increment("omniauth.failure", ...)`.
