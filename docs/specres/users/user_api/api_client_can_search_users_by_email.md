---
id: "01KJ9N1KSANXHPTEEVE4VDJ2V8"
name: "api_client_can_search_users_by_email"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/concerns/api/users_controller.rb`
- `spec/requests/api/v1/users_spec.rb` (Test)

## Functional Overview

An authenticated API client with super-admin privileges can look up a single Forem user by their exact email address via `GET /api/users/search?email=<address>`. The endpoint enforces the `search_by_email?` Pundit policy, so any caller without the required role receives an unauthorized response. When a matching user is found the response is the same JSON user representation used by the profile retrieval endpoint. When the email parameter is absent or no user matches the address, the endpoint returns 404.

## Design Intent

Restricting search to exact email lookup behind an admin-only policy prevents bulk enumeration of users through the public API. Reusing the `show` template keeps the response shape consistent with the rest of the Users API and avoids a separate serialization path.

## Key Members

- `GET /api/users/search` — the route that maps to this action
- `params[:email]` — the required query parameter carrying the address to look up
- `search_by_email?` — Pundit policy method that gates access; only super-admins pass

## Scenarios

### Successful search

1. An API client sends `GET /api/users/search?email=<address>` with a valid super-admin API key.
2. The system authorizes the request via the `search_by_email?` policy.
3. The system looks up the user by the exact email address provided.
4. The system responds with HTTP 200 and a JSON body representing the user (same shape as `GET /api/users/:id`).

### User not found

1. An API client sends `GET /api/users/search?email=unknown@example.com` with a valid super-admin API key.
2. The system authorizes the request.
3. No user exists with that email address.
4. The system responds with HTTP 404.

### No email parameter provided

1. An API client sends `GET /api/users/search` (no `email` query parameter) with a valid super-admin API key.
2. The system authorizes the request.
3. Because no email was supplied, the system responds immediately with HTTP 404 without performing a database lookup.

### Unauthorized — non-admin API key

1. An API client sends `GET /api/users/search?email=<address>` with an API key that belongs to an ordinary (non-admin) user.
2. The `search_by_email?` policy check fails.
3. The system responds with HTTP 401.

## Failures / Exceptions

- No API key or an invalid API key results in HTTP 401 before the policy check is reached.
- The endpoint performs an exact match on `email`; partial or case-folded matches are not supported by this action.
