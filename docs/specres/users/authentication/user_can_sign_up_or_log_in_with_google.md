---
id: "01KJBKA8M437QKNGFD6ZDS458V"
name: "user_can_sign_up_or_log_in_with_google"
status: "draft"
---

## Related Files

- `app/services/authentication/providers/google_oauth2.rb`
- `app/services/authentication/providers/provider.rb` (Base class)

## Functional Overview

When a user chooses to sign in or register via Google, Forem initiates an OAuth 2.0 flow through the `Authentication::Providers::GoogleOauth2` provider. Upon receiving the OAuth callback, the provider maps the Google account's profile data — display name, email address, and profile image — to Forem user attributes. Because Google accounts have no username or nickname concept, the provider synthesises a deterministic username by combining the user's display name (with a space replaced by an underscore) and a SHA-512 hash of the Google UID, truncated to 25 characters. If the profile image URL is present it is validated through `Images::SafeRemoteProfileImageUrl` before being stored. Existing users receive only a refreshed `google_oauth2_username`; new users additionally receive name, email, and remote profile image.

## Design Intent

Google does not expose a stable username or nickname in its OAuth payload, unlike GitHub. Rather than leaving the username field blank or letting two users collide on a common first name, the provider derives a username that is both human-readable and collision-resistant: the name portion anchors it to the person, while the UID-derived hash suffix makes it unique across all Google accounts. The randomised fallback (8 uppercase letters) is used only when `info.name` is absent, providing a safe default without failing the login.

## Scenarios

### New user signs up with Google

1. User clicks "Sign in with Google" and authorises the Forem application in the Google consent screen.
2. Google redirects back with an OAuth2 callback containing the user's display name, email, profile image URL, and a unique Google UID.
3. The provider constructs a `google_oauth2_username` from the display name and a hash of the UID (truncated to 25 characters).
4. The profile image URL is passed through the safe-remote-URL validator before being stored.
5. A new Forem account is created with the mapped name, email, profile image, and generated username.
6. The user is signed in and redirected to their new profile.

### Existing user logs in with Google

1. User clicks "Sign in with Google" and the OAuth2 callback identifies a matching Forem account.
2. The provider refreshes only the `google_oauth2_username` from the latest OAuth payload; name, email, and profile image are not overwritten.
3. The user is signed in and returned to their session.

### Google account has no display name

1. During sign-up or login the OAuth payload contains no `info.name` value.
2. The provider falls back to a random 8-character uppercase string as the `google_oauth2_username`.
3. Authentication proceeds normally with the fallback username.

### Google account has no profile image

1. The OAuth callback contains no profile image URL.
2. `Images::SafeRemoteProfileImageUrl` receives a blank or nil value and returns a safe default (or nil).
3. The user account is created or updated without a remote profile image; no error is raised.

## Failures / Exceptions

- If `info.name` is nil or blank, `user_nickname` returns nil, and the provider substitutes a random 8-character string to ensure `google_oauth2_username` is always populated.
- `cleanup_payload` is a no-op for this provider (returns the payload unchanged), meaning no sensitive OAuth fields are stripped at the provider level; any sensitive-data handling is delegated to higher layers.
