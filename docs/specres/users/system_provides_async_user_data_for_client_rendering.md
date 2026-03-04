---
id: "01KJVM8M6XFS8FZ49N49XXD9SM"
name: "system_provides_async_user_data_for_client_rendering"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/models/async_info.rb`
- `app/controllers/async_info_controller.rb`
- `app/views/async_info/navigation_links.html.erb` (Template)
- `spec/models/async_info_spec.rb` (Test)
- `spec/requests/async_info_spec.rb` (Test)

## Functional Overview

The system exposes two asynchronous endpoints that supply client-side JavaScript with the data it needs to render a personalised UI without blocking the initial page load. The `base_data` endpoint returns a JSON payload containing CSRF tokens, broadcast announcements, and — for authenticated users — a rich user hash assembled by `AsyncInfo`, plus geolocation, email opt-in eligibility, and creator status. The user hash is served from a versioned Rails cache keyed on the user and the current subforem, expiring after 15 minutes. The `navigation_links` endpoint returns a fragment of HTML (no layout) containing the search link, a conditional authentication widget, and the main navigation partial, intended for injection into the mobile hamburger menu.

## Design Intent

Separating async data from the initial HTML render keeps the synchronous page delivery fast: the JavaScript bootstrapper calls `base_data` immediately after load to hydrate user-specific state. The controller intentionally has no Pundit policy because both endpoints must be reachable by unauthenticated visitors — the user-specific branch is guarded by session verification in code rather than by an authorization layer. Caching the user hash avoids reassembling the same data on every tab focus or route change.

## Key Members

- `AsyncInfo.to_hash(user:, context:)` — class-level entry point that builds the full user data hash; delegates policy visibility checks to the given controller context
- `policies` — an array of hashes, each with `dom_class` (CSS selector used by the front-end) and `visible` (boolean derived from the Pundit policy for the current user), covering Article create and moderate permissions
- `NUMBER_OF_MINUTES_FOR_CACHE_EXPIRY` — 15-minute TTL applied to the cached user hash in `user_data`

## Scenarios

### Unauthenticated visitor requests base data

1. A visitor (not signed in) sends `GET /async_info/base_data`.
2. The system discards any leftover flash notice.
3. The system responds with JSON containing only `broadcast`, `param` (CSRF param name), and `token` (CSRF token).
4. No user data, geolocation, or creator flag is included.

### Authenticated user requests base data

1. A signed-in user sends `GET /async_info/base_data`.
2. The system verifies the session state; if the session is invalid the user is signed out and the unauthenticated path is followed.
3. The system records the user's presence (`update_presence!`).
4. The system assembles the response: CSRF tokens, broadcast data, geolocation header, email opt-in eligibility, creator flag, and the cached `AsyncInfo` user hash.
5. The user hash includes identity fields, followed tags and podcasts, reading list, blocked user IDs, onboarding flags, moderation roles, feed style, policy visibility array, and Apple-relay auth flag.
6. The full JSON payload is returned to the client.

### Client resolves article policy visibility

1. `AsyncInfo#to_hash` asks the controller context to evaluate the Pundit policy for `Article` against `create?` and `moderate?`.
2. For each query, the system derives a `dom_class` string (e.g. `js-policy-article-create`) and a `visible` boolean.
3. If the policy raises `Pundit::NotAuthorizedError`, `visible` is set to `false` without propagating the error.
4. The resulting `policies` array is embedded in the user hash.

### Request for navigation links fragment

1. Any visitor sends `GET /async_info/navigation_links`.
2. The response is served with cache-control headers set by `set_cache_control_headers`.
3. The system renders `async_info/navigation_links.html.erb` without a layout wrapper.
4. The fragment includes a search link, an authentication widget (only if not signed in), and the main navigation partial in hamburger context.

## Failures / Exceptions

- If `verify_state_of_user_session?` finds `last_sign_in_at` is present but `current_sign_in_at` is blank, the user is signed out and the response falls through to the unauthenticated branch.
- If the Pundit policy raises `Pundit::NotAuthorizedError` during policy visibility resolution, the error is rescued and `visible` is returned as `false`.
