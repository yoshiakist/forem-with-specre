---
id: "01KJBK9XFXRJW99630DW673YSQ"
name: "user_can_sign_up_or_log_in_with_twitter"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/authentication/providers/twitter.rb`
- `spec/services/authentication/providers/twitter_spec.rb` (Test)
- `spec/system/authentication/user_logs_in_with_twitter_spec.rb` (Test)

## Functional Overview

When a user initiates Twitter (X) OAuth, the Twitter provider maps the OmniAuth payload to Forem user attributes. For new users it extracts the display name (preferring `raw_info.name`), a full-resolution profile image URL (by stripping the `_normal` suffix), the email address if Twitter supplies one, and the Twitter username (`info.nickname`). For returning users it updates only the stored Twitter username. The provider also sanitises the payload by removing the server-side OAuth access token keys before any data is persisted. Sign-in paths always include `secure_image_url=true` to force HTTPS profile images. The shared OmniAuth callback infrastructure (controller, `Authenticator`, `Identity` model) is documented in the `user_can_sign_up_or_log_in_with_github` card.

## Design Intent

Twitter does not guarantee that it will supply an email address in the OAuth payload. The provider handles this gracefully by coercing the value to a string (`info.email.to_s`), which yields an empty string rather than `nil`, letting downstream validation decide what to do. The `secure_image_url: true` mandatory parameter is required by the `omniauth-twitter` gem to return HTTPS image URLs; this is enforced unconditionally so callers cannot accidentally disable it.

## Scenarios

### New user signs up via Twitter

1. An unauthenticated visitor clicks "Continue with Twitter" on the sign-up page.
2. Twitter OAuth completes and the callback delivers a payload with the user's name, nickname, profile image, and optional email.
3. The system creates a new Forem account, sets `twitter_username`, populates a full-resolution profile image, stores the email when available, and redirects the user to the onboarding flow.
4. A remember token is issued so the session persists across browser restarts.

### New user signs up when their Twitter username is already taken

1. A visitor completes Twitter OAuth but another Forem account already holds the derived username.
2. The system creates the new account with a temporary username (the existing username with a disambiguating suffix) and redirects to onboarding.

### Returning user logs in via Twitter

1. A user with an existing Forem account and a linked Twitter identity clicks "Continue with Twitter".
2. The provider looks up the existing identity by the Twitter UID and updates only `twitter_username` on the user record.
3. The user is redirected to the home feed with `?signin=true`.

### Twitter OAuth fails or returns invalid credentials

1. The OAuth callback returns an error (e.g., user denies access, token is invalid, or an `OAuth::Unauthorized` is raised).
2. No user account is created or modified.
3. The user is redirected back to the sign-in page.
4. The failure is reported to Datadog via `ForemStatsClient.increment("omniauth.failure", ...)`.

## Failures / Exceptions

- If Twitter returns a name longer than 100 characters, the resulting `User` record fails validation. The system does not create the account, redirects back to the sign-up page, and notifies Honeybadger.
- If the community is in invite-only mode, the "Continue with Twitter" button is not shown and Twitter authentication is unavailable to new users.
- The provider removes `extra.access_token` from the OmniAuth payload before it can be stored, preventing accidental persistence of server-side OAuth credentials.
