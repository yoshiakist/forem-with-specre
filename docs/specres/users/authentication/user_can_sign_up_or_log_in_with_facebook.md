---
id: "01KJBKE6FH7TS0RJVRWB313W9Z"
name: "user_can_sign_up_or_log_in_with_facebook"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/authentication/providers/facebook.rb`
- `spec/services/authentication/providers/facebook_spec.rb` (Test)
- `spec/system/authentication/user_logs_in_with_facebook_spec.rb` (Test)

## Functional Overview

When a user initiates sign-up or login via Facebook, the platform uses the `Authentication::Providers::Facebook` provider — a subclass of the shared `Authentication::Providers::Provider` base — to extract and map data from the Facebook Graph API OmniAuth response. For new users, the provider maps the Facebook display name, email address (which Facebook may withhold), and a remotely hosted profile image; it also synthesizes a unique Forem username by combining the display name with a SHA-512-derived suffix of the user's Facebook UID, since Facebook has no concept of a username or nickname. For returning users, the provider updates only the `facebook_username` field to reflect the current display name. The shared OmniAuth infrastructure (documented in `user_can_sign_up_or_log_in_with_github`) handles session creation, onboarding redirection, and error reporting.

## Design Intent

Facebook does not expose a username or nickname field in its Graph API response. To satisfy the Forem requirement that every user have a unique username, the provider constructs one deterministically: it replaces the first space in the display name with an underscore, then appends a prefix of the SHA-512 hex digest of the Facebook UID. The combined string is truncated to 25 characters. Using the UID as the hash input guarantees that the same Facebook account always produces the same suffix, while the hash length provides enough entropy to avoid collisions in practice.

## Scenarios

### New user signs up with Facebook and grants email permission

1. User visits the sign-up page and clicks "Continue with Facebook".
2. Facebook redirects back with a valid OmniAuth payload that includes the user's name, email, and profile image URL.
3. The platform maps the name, email, and a safe HTTPS profile image URL to the new user record.
4. A `facebook_username` is synthesised from the display name and a hash of the Facebook UID, then truncated to 25 characters.
5. A new user account is created, a remember-me token is set, and the user is redirected to `/onboarding`.

### New user signs up with Facebook but withholds email permission

1. User visits the sign-up page and clicks "Continue with Facebook".
2. Facebook redirects back with a valid OmniAuth payload that omits the email field.
3. The provider sets the email attribute to an empty string and proceeds with account creation.
4. A new user account is created and the user is redirected to `/onboarding`.

### Existing user logs in with Facebook

1. User visits the sign-up page and clicks "Continue with Facebook".
2. Facebook redirects back with a valid OmniAuth payload matching the user's existing identity.
3. The provider updates `facebook_username` with the current Facebook display name.
4. The user is logged in and redirected to `/?signin=true`.

### Authentication fails due to invalid or denied credentials

1. User visits the sign-up page and clicks "Continue with Facebook".
2. The OmniAuth callback returns an error (e.g., denied access, OAuth unauthorized, or no error object present).
3. No user account is created or updated.
4. The platform records the failure metric in Datadog (`omniauth.failure`) and redirects the user to the sign-in page.

## Failures / Exceptions

- If the Facebook name exceeds 100 characters, model validation fails: no user is created, the platform notifies Honeybadger, and the user is redirected to the registration page.
- If the inferred Forem username is already taken by another account, the system creates the new user with the hashed suffix in the username, preserving uniqueness without blocking sign-up.
- In invite-only mode, the Facebook authentication option is not displayed on the sign-up page at all; attempting to access it directly redirects appropriately.
