---
id: "01KJ9MTBJ0F7WTG0KSNXPGF3N9"
name: "api_client_can_retrieve_user_profile"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/concerns/api/users_controller.rb`
- `app/controllers/api/v0/users_controller.rb`
- `app/controllers/api/v1/users_controller.rb`
- `spec/requests/api/v0/users_spec.rb` (Test)
- `spec/requests/api/v1/users_spec.rb` (Test)
- `spec/requests/api/v1/docs/users_spec.rb` (Test)

## Functional Overview

The API exposes two endpoints for retrieving user profile data: `GET /api/users/:id` (the `show` action) and `GET /api/users/me` (the `me` action). The `show` action accepts either a numeric user ID or the special value `by_username` with a `url` query parameter to look up by username; it returns a public profile and responds with 404 for unregistered users. The `me` action requires authentication and returns the profile of the currently authenticated user. Both endpoints are available in the v0 and v1 APIs, with v1 requiring an API key for the `me` action. The response includes standard profile fields (username, name, social handles, bio, location, profile image, join date) and, in v1, additional fields such as `badge_ids` and — for the `me` endpoint — `followers_count`. The email field is included in the response only when the user has opted in to displaying it publicly.

## Key Members

- `SHOW_ATTRIBUTES_FOR_SERIALIZATION` — fixed list of scalar user columns eagerly selected for the `show` response (id, username, name, summary, twitter_username, github_username, website_url, location, created_at, profile_image, registered).
- `params[:id]` — either a numeric user ID or the literal string `"by_username"`.
- `params[:url]` — the username to look up when `params[:id]` is `"by_username"`.
- `display_email_on_profile` (user setting) — gates whether the email field is populated in the response.

## Scenarios

### Retrieve a public user profile by numeric ID

1. Client sends `GET /api/users/:id` with a valid numeric user ID.
2. The system looks up the user (joining profile and setting tables) and verifies the user is registered.
3. The system returns 200 with a JSON object containing the user's public profile fields (type_of, id, username, name, social handles, bio, website URL, location, join date, and profile image URL).

### Retrieve a public user profile by username

1. Client sends `GET /api/users/by_username` with a `url` query parameter containing a valid username.
2. The system looks up the user by username and verifies they are registered.
3. The system returns 200 with the same public profile JSON as the ID-based lookup.

### Retrieve the authenticated user's own profile

1. Client sends `GET /api/users/me` with a valid API key in the `api-key` header.
2. The system authenticates the request and identifies the requesting user.
3. The system returns 200 with the user's profile JSON; in v1 the response additionally includes `badge_ids` and `followers_count` (excluding followers marked as spam).

### Email field visibility in the profile response (v1)

1. Client sends `GET /api/users/:id` or `GET /api/users/by_username` via the v1 API.
2. If the user has enabled `display_email_on_profile`, the `email` field in the response contains the user's email address.
3. If the user has not enabled that setting, the `email` key is present in the response but its value is null.

## Failures / Exceptions

- Requesting a non-existent user ID or an unknown username returns 404.
- Requesting a user who exists but is not registered (`registered: false`) returns 404.
- Requesting `GET /api/users/me` without a valid API key returns 401.
- On a private Forem instance, unauthenticated requests to `GET /api/users/:id` return 401; authenticated requests via `me` still succeed.
