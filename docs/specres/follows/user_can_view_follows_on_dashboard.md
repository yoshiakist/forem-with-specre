---
id: "01KJ1XAJ69KXNBRJE9Z3328GT0"
name: "user_can_view_follows_on_dashboard"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/followings_controller.rb`
- `app/views/dashboards/following_users.html.erb` (Template)
- `app/views/dashboards/following_tags.html.erb` (Template)
- `spec/requests/followings_spec.rb` (Test)
- `spec/requests/follows_bulk_update_spec.rb` (Test)
- `spec/system/dashboards/user_scrolls_down_dashboard_follows_spec.rb` (Test)

## Functional Overview

Authenticated users can view their following lists for users and tags via dedicated dashboard pages. The `FollowingsController#users` action returns the current user's followed users in reverse chronological order, serialized as JSON with identity and profile image fields. The `FollowingsController#tags` action returns followed tags, splitting them into two lists based on `explicit_points`: tags with a non-negative score appear on the standard following-tags page, while tags with a negative score appear on the hidden-tags page. Both actions support paginated infinite scroll via `load_follows_and_paginate`, which respects a `per_page` query parameter bounded by a maximum of 1000. Unauthenticated requests to either endpoint are rejected with an HTTP 401 response.

## Design Intent

Separating followed tags into "following" and "hidden" lists by the sign of `explicit_points` lets users tune their feed without unfollowing a tag entirely — a negative explicit weight suppresses content from that tag while preserving the follow relationship for future adjustment.

## Key Members

- `ATTRIBUTES_FOR_SERIALIZATION` — minimal set of follow fields (`id`, `followable_id`, `followable_type`) selected for users
- `TAGS_ATTRIBUTES_FOR_SERIALIZATION` — extends the base set with `points` and `explicit_points` for tag follows
- `@follows_limit` — resolved page size, capped at 1000, shared across all actions via `before_action`

## Scenarios

### Authenticated user views their followed users

1. An authenticated user navigates to `GET /followings/users`.
2. The controller fetches the user's follows of type `User`, ordered newest first, and paginates the result.
3. The response returns HTTP 200 with a JSON array; each entry includes `type_of: "user_following"`, the follow `id`, and the followed user's `name`, `username`, `path`, and `profile_image`.
4. The dashboard template renders each followed user as a card with avatar and profile link; if the list is empty, an empty-state message is shown instead.

### Authenticated user views their followed tags (standard list)

1. An authenticated user navigates to `GET /followings/tags` with `controller_action=following_tags` (or no filter).
2. The controller fetches follows of type `ActsAsTaggableOn::Tag` where `explicit_points >= 0`, ordered newest first, and paginates the result.
3. The response returns HTTP 200 with a JSON array; each entry includes `type_of: "tag_following"`, the follow `id`, `name`, `points`, `explicit_points`, `token`, and `color`.
4. The dashboard template renders the tag list; if empty, a prompt to explore tags is shown.

### Authenticated user views their hidden tags

1. An authenticated user navigates to `GET /followings/tags` with `controller_action=hidden_tags`.
2. The controller filters tag follows to those with `explicit_points < 0`, ordered newest first, and paginates the result.
3. The response returns HTTP 200 with only the negatively-weighted tag follows.

### User scrolls to load more follows (infinite scroll)

1. An authenticated user visits a following dashboard page (users or tags) with a `per_page` query parameter smaller than the total number of follows.
2. The page loads the first batch of follow cards rendered as `div` elements with ids prefixed `follows-`.
3. As the user scrolls to the bottom, the frontend fetches the next page, and additional cards appear until all follows are loaded.

### Unauthenticated access is rejected

1. An unauthenticated visitor requests `GET /followings/users` or `GET /followings/tags`.
2. The `authenticate_user!` before-action halts the request and returns HTTP 401.

## Failures / Exceptions

- Requests from users who do not own a given follow are rejected; attempting a bulk update on another user's follow raises `Pundit::NotAuthorizedError`.
