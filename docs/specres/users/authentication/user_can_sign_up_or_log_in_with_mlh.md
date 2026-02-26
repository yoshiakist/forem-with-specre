---
id: "01KJBKEF96PT34KK0QAPBGFP6F"
name: "user_can_sign_up_or_log_in_with_mlh"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/authentication/providers/mlh.rb`
- `spec/services/authentication/providers/mlh_spec.rb` (Test)

## Functional Overview

When a user initiates sign-up or log-in via the MyMLH OAuth flow, the MLH provider maps the OmniAuth payload to Forem user attributes. For new users, it extracts `email`, `mlh_username` (from the OAuth `nickname` field), and `name`. For returning users, it refreshes only the `mlh_username`. Unlike other providers, the MLH sign-in path does not append a `callback_url` query parameter — the callback URL must be registered directly in the MyMLH developer portal and matched by OmniAuth's configured route.

## Design Intent

MLH requires that the OAuth callback URL be pre-registered in the MyMLH application settings and matched exactly. Injecting a dynamic `callback_url` query parameter (as some other providers allow) would break this strict matching requirement. Omitting the parameter keeps the redirect URL stable and consistent with what is registered at `https://my.mlh.io/oauth/applications`.

## Scenarios

### New user signs up via MyMLH

1. User clicks the MyMLH sign-in button; the browser is redirected to the MyMLH OAuth authorization page.
2. After the user grants permission, MyMLH redirects back to Forem's configured OmniAuth callback URL with a payload containing the user's email, nickname, and name.
3. The MLH provider extracts `email`, `mlh_username` (from `nickname`), and `name` from the payload and makes them available for account creation.
4. Forem creates a new user account using those attributes.

### Existing user logs in via MyMLH

1. User clicks the MyMLH sign-in button and completes the OAuth flow.
2. The MLH provider identifies the returning user by their MLH UID.
3. Only `mlh_username` is refreshed on the existing user record; email and display name are not overwritten.

### Sign-in path does not include a callback_url parameter

1. When Forem constructs the link to begin the MyMLH OAuth flow, the path is generated without appending a `callback_url` query parameter.
2. OmniAuth uses its internally configured callback route, ensuring the redirect URI matches the URL registered in the MyMLH developer portal exactly.

### Sign-in path accepts additional query parameters

1. Callers may pass arbitrary keyword arguments (e.g., `state`) to `sign_in_path`.
2. Those parameters are forwarded as query string values on the resulting path, allowing state or other OAuth hints to be threaded through without affecting the absence of `callback_url`.

## Failures / Exceptions

- If the OmniAuth payload does not include an email, `email` is coerced to an empty string (`info.email.to_s`) rather than `nil`; downstream code is responsible for validating presence.
- `cleanup_payload` is a no-op for MLH — the raw payload is passed through unchanged, meaning no sensitive fields are stripped at this layer.
