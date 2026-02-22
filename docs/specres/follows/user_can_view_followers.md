---
id: "01KJ1XA9ETJ0A7Y8MWW28NFSN8"
name: "user_can_view_followers"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/concerns/api/followers_controller.rb`
- `app/controllers/api/v0/followers_controller.rb`
- `app/controllers/api/v1/followers_controller.rb`
- `app/views/dashboards/followers.html.erb` (Template)
- `app/controllers/dashboards_controller.rb` (Tagged: 01KHZGV8H4BG6XE1A7T06AVD4X)
- `spec/requests/api/v0/followers_spec.rb` (Test)
- `spec/requests/api/v1/followers_spec.rb` (Test)
- `spec/requests/api/v1/docs/followers_spec.rb` (Test)
- `spec/system/dashboards/user_followers_display_spec.rb` (Test)

## Functional Overview

Authenticated users can retrieve a paginated list of their followers via the API (`GET /api/followers/users`) or browse them on their dashboard at `/dashboard/user_followers`. The API is available under both v0 and v1, both requiring authentication via API key or current session. Results include each follower's profile details (name, username, path, profile image) and are ordered by follow date descending by default; the caller may request ascending order via a `sort` query parameter. Pagination is supported through `page` and `per_page` parameters, with a default of 80 per page and a maximum of 1000. Only non-suspended follow relationships are returned. The dashboard view renders follower cards in a responsive grid, showing each follower's avatar, name, and username, or an empty-state message when there are no followers.

## Design Intent

The shared concern `Api::FollowersController` centralises the query logic so that both v0 and v1 controllers include identical behavior without duplication. `Follow.non_suspended` ensures suspended users are filtered out before results reach the caller. The `JsonApiSortParam` concern is included to allow flexible, safe sort-direction control with an allowlist limited to `created_at`, preventing arbitrary column injection.

## Key Members

- `@follows_limit` — effective per-page size, capped to the configured maximum (1000)
- `USERS_ATTRIBUTES_FOR_SERIALIZATION` — allowlist of columns selected from `follows` to limit data exposure: `id`, `follower_id`, `follower_type`, `created_at`
- `sort` query parameter — controls sort direction; omit for descending, pass `created_at` for ascending

## Scenarios

### Unauthorized request is rejected

1. A client sends `GET /api/followers/users` without an API key or active session.
2. The system returns an HTTP 401 Unauthorized response.

### Authenticated user retrieves their followers

1. A user authenticates with an API key or an active session.
2. The client sends `GET /api/followers/users`.
3. The system queries non-suspended follows targeting the authenticated user, eagerly loading follower profiles.
4. The response contains an array of follower objects, each with `type_of`, `id`, `name`, `path`, `username`, and `profile_image` fields.
5. Results are ordered by follow date descending by default.

### Caller overrides sort direction

1. An authenticated client sends `GET /api/followers/users?sort=created_at`.
2. The system interprets the `sort` parameter as ascending order on `created_at`.
3. The response list is ordered from oldest to newest follow relationship.

### Caller paginates results

1. An authenticated client sends `GET /api/followers/users?page=1&per_page=1`.
2. The system returns the first page containing exactly one follower.
3. Subsequent requests with `page=2` return the next follower; a page beyond the last returns an empty array.

### User views followers on the dashboard

1. An authenticated user navigates to `/dashboard/user_followers`.
2. The dashboard controller loads the user's non-suspended followers.
3. If followers exist, the view renders a responsive card grid showing each follower's avatar, name, and username with links to their profile.
4. If the user has no followers, the view displays an empty-state message.

## Failures / Exceptions

- Requests without authentication (no API key, no active session) receive HTTP 401 Unauthorized.
- The `per_page` value is silently capped at 1000; values exceeding the maximum are reduced rather than rejected.
