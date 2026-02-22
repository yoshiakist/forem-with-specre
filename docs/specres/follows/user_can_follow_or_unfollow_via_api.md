---
id: "01KJ1X77PBDY9JBNX09TV75B95"
name: "user_can_follow_or_unfollow_via_api"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/concerns/api/follows_controller.rb`
- `app/controllers/api/v0/follows_controller.rb`
- `app/controllers/api/v1/follows_controller.rb`
- `spec/requests/api/v0/follows_spec.rb` (Test)
- `spec/requests/api/v1/follows_spec.rb` (Test)
- `spec/requests/api/v1/docs/follows_spec.rb` (Test)
- `spec/requests/api/v1/docs/followed_tags_spec.rb` (Test)

## Functional Overview

Authenticated users can follow one or more other users and/or organizations in a single API call via `POST /api/follows`. The shared concern `Api::FollowsController` handles the logic for both v0 and v1 endpoints: it extracts user IDs and organization IDs from the request parameters (supporting both array-of-integers and array-of-objects formats for compatibility), then enqueues a `Users::FollowWorker` background job for each target. The endpoint returns a JSON response reporting how many followables were processed. A companion `GET /api/follows/tags` endpoint returns the list of tags the authenticated user already follows, ordered by follow weight descending. Both endpoints require authentication via API key or session cookie.

## Design Intent

The parameter extraction logic intentionally supports two input shapes (`user_ids: [1, 2]` and `users: [{id: 1}, {id: 2}]`) to work around a known incompatibility between rswag's OpenAPI documentation generation and Rails strong parameters when dealing with arrays of objects. This dual-format tolerance keeps the API documented in Swagger while preserving backward compatibility with existing clients.

## Key Members

- `user_ids` — list of user IDs to follow, extracted from either `user_ids` or `users[*].id` in the request params
- `org_ids` — list of organization IDs to follow, extracted from either `organization_ids` or `organizations[*].id` in the request params
- `Users::FollowWorker` — background job that creates the actual follow relationship; called asynchronously for each target

## Scenarios

### Authenticated user follows multiple users

1. An authenticated user sends `POST /api/follows` with a list of user IDs (as either an array of integers or an array of objects with an `id` field).
2. The server enqueues one `Users::FollowWorker` background job per requested user ID, with the followable type set to `"User"`.
3. The server responds with a JSON body containing an `outcome` field reporting the total count of followables queued.

### Authenticated user follows multiple organizations

1. An authenticated user sends `POST /api/follows` with a list of organization IDs.
2. The server enqueues one `Users::FollowWorker` background job per organization ID, with the followable type set to `"Organization"`.
3. The response `outcome` field reflects the total number of users and organizations queued in the same request.

### Authenticated user follows both users and organizations in one request

1. An authenticated user sends `POST /api/follows` supplying both `users` and `organizations` arrays in the same request.
2. The server enqueues follow jobs for every entry across both lists.
3. The `outcome` count in the response equals the sum of users and organizations provided.

### Authenticated user retrieves their followed tags

1. An authenticated user sends `GET /api/follows/tags`.
2. The server queries the user's follow records where the followable type is `ActsAsTaggableOn::Tag`, loading each tag's id, name, and follow weight.
3. The server returns a JSON array of tag objects ordered by follow weight descending.

## Failures / Exceptions

- Unauthenticated requests to either `POST /api/follows` or `GET /api/follows/tags` receive a `401 Unauthorized` response.
