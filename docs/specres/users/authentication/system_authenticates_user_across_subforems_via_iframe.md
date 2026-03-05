---
id: "01KJVJ0CDYZE89Q4THGRC8XPCR"
name: "system_authenticates_user_across_subforems_via_iframe"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/auth_pass_controller.rb`
- `app/views/auth_pass/iframe.html.erb` (Template)
- `spec/requests/auth_passes_spec.rb` (Test)

## Functional Overview

When a user visits a subforem, the subforem page embeds a hidden iframe pointing to the main domain's `GET /auth_pass/iframe` endpoint. That endpoint verifies the requesting host is a known subforem domain, then attempts to identify the user through three layers: the main Devise session, an iframe-specific session cookie (backed by a separate session store to allow cross-site cookies), and a signed `user_id` cookie from the main domain. If the user is found through any of these paths, a short-lived JWT (5-minute expiry) is generated and sent to the parent window via `postMessage`. The subforem's JavaScript receives the token and calls `POST /auth_pass/token_login` on its own domain, which decodes the JWT, locates the user, sets a Devise remember-me cookie scoped to the subforem's root domain, and also sets the `forem_user_signed_in` cookie — establishing a persistent authenticated session on the subforem without any separate login step.

## Design Intent

Subforems run on separate domains, so Devise sessions and cookies do not carry across. The iframe technique exploits the fact that a browser will send cookies to the main domain even when the request originates from an iframe inside a subforem page. A short-lived JWT bridges the trust gap: the main domain vouches for the user by signing the token, and the subforem accepts it within the 5-minute window. Using a dedicated iframe session store (different `SameSite` and `Secure` settings) allows the cross-origin cookie to be written while keeping the main application session secure.

## Key Members

- `@token` — JWT string set in the iframe action and rendered into the template; empty when no authenticated user is found
- JWT payload — contains `user_id` (integer) and `exp` (Unix timestamp 5 minutes in the future)
- `remember_user_token` cookie — Devise remember-me cookie set with a domain scoped to the subforem's root domain (e.g., `.example.com`)
- `forem_user_signed_in` cookie — boolean flag cookie set alongside the remember cookie to signal authenticated state to client-side code

## Scenarios

### User is authenticated on the main domain (Devise session present)

1. The subforem page loads the main domain's `/auth_pass/iframe` in a hidden iframe.
2. The iframe action confirms the requesting host is a registered subforem domain.
3. The action finds the current Devise session user and verifies they have not explicitly signed out.
4. A JWT token (5-minute expiry) is generated and stored in `@token`.
5. The iframe template renders a script that calls `window.parent.postMessage` with `authenticated: true` and the token.
6. The subforem's JavaScript receives the message and posts the token to `POST /auth_pass/token_login`.
7. The token_login action decodes the JWT, finds the user, sets the Devise remember cookie with the correct root domain, and responds with `{ success: true }`.

### User has a valid iframe session cookie (returning cross-origin visitor)

1. The subforem page embeds the `/auth_pass/iframe` iframe.
2. The browser sends the iframe-specific session cookie to the main domain; the action reads `session[:user_id]`.
3. The user record is found; a new JWT is generated and sent via `postMessage`.
4. The subforem JavaScript exchanges the token via `POST /auth_pass/token_login`, which refreshes the remember cookie.

### User is not signed in through session but has a signed `user_id` cookie

1. The iframe action finds no active Devise session and no iframe session entry.
2. It reads the signed `user_id` cookie from the main domain's cookie jar.
3. The corresponding user is found, stored in the iframe session, and a JWT is generated.
4. Authentication proceeds as in the main-domain-session scenario above.

### User is not authenticated on any domain

1. The iframe action finds no session user, no iframe session entry, and no signed cookie.
2. The action renders an empty HTML page with HTTP 200.
3. The iframe template is not rendered; no `postMessage` is sent.
4. The subforem remains in an unauthenticated state.

### Subforem domain is not registered

1. The request host is not found in `Subforem.cached_all_domains`.
2. The action responds with HTTP 401 `Unauthorized` immediately, before any user lookup.

## Failures / Exceptions

- **Invalid or expired JWT at `POST /auth_pass/token_login`**: The action returns HTTP 401 with `{ success: false, error: "Invalid or expired token" }`.
- **User record deleted between token issuance and `token_login`**: The action returns HTTP 401 with `{ success: false, error: "User not found" }`.
- **User explicitly signed out (`current_sign_in_at` is blank)**: `user_not_signed_out?` returns false; the iframe action renders an empty body and no token is issued.
- **Unregistered iframe session user_id**: The stale `session[:user_id]` is deleted and an empty body is returned.
- **Request from an unregistered origin**: CORS headers are not set; the browser will block the cross-origin response.
