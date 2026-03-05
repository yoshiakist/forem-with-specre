---
id: "01KJ9K792FM0FA2QSE1BE6N7AE"
name: "user_can_block_another_user"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/user_blocks_controller.rb`
- `app/models/user_block.rb`
- `app/policies/user_block_policy.rb`
- `spec/requests/user_blocks_spec.rb` (Test)
- `spec/models/user_block_spec.rb` (Test)
- `spec/factories/user_blocks.rb` (Test)

## Functional Overview

Authenticated users can block other users through the `UserBlock` model and `UserBlocksController`. Blocking creates a directional relationship between a blocker and a blocked user, automatically removes any existing follow relationships in both directions, and maintains a cache of blocked user IDs for fast lookup. Users can also query whether a specific user is currently blocked, and unblock users to destroy the block record. Only non-spam, non-suspended users are permitted to create or destroy blocks. The system tracks block counts on both parties via counter cache columns.

## Design Intent

Blocking is intentionally directional and unidirectional — the blocker's perspective determines which content is hidden. The cached blocked IDs list (keyed per blocker, expiring after 48 hours and invalidated on create/destroy) is designed for high-read performance to filter out blocked content across the platform without per-request database queries.

## Key Members

- `blocker_id` — ID of the user who initiated the block
- `blocked_id` — ID of the user being blocked; must differ from `blocker_id`
- `config` — block configuration; currently only `"default"` is valid
- `blocking_others_count` — counter cache on the blocker indicating how many users they have blocked
- `blocked_by_count` — counter cache on the blocked user indicating how many times they have been blocked
- `BLOCKED_IDS_CACHE_KEY` — cache key prefix `"blocked_ids_for_blocker/"` used for the 48-hour blocked-ID cache

## Scenarios

### User checks whether another user is blocked

1. Authenticated user sends a request to check the block status for a given user ID.
2. System looks up whether a block record exists with the current user as blocker and the target as blocked.
3. System responds with `"blocking"` if a block exists, or `"not-blocking"` otherwise.

### User successfully blocks another user

1. Authenticated, non-suspended user submits a request to block a target user.
2. System creates a `UserBlock` record with the current user as blocker and the target as blocked, setting config to `"default"`.
3. System removes any follow relationship from the blocker to the blocked user and vice versa.
4. System responds with `"blocked"`.

### User unblocks a previously blocked user

1. Authenticated user submits a request to unblock a target user.
2. System locates the matching `UserBlock` record owned by the current user.
3. System destroys the record and busts the blocker's cached block list.
4. System responds with `"unblocked"`.

### Unauthenticated request is rejected

1. An unauthenticated client sends any request to the user blocks endpoints.
2. System responds with HTTP 401 and result `"not-logged-in"`.

### Unblock attempted when no blocks exist

1. Authenticated user sends an unblock request when their `blocking_others_count` is zero.
2. System short-circuits without querying for a block record.
3. System responds with `"not-blocking-anyone"`.

## Failures / Exceptions

- A user cannot block themselves; the model validation rejects records where `blocker_id` equals `blocked_id`.
- Duplicate block records are rejected by a uniqueness validation scoped to `[blocker_id, blocked_id]`.
- Only `"default"` is a valid value for `config`; other values are rejected by inclusion validation.
- Suspended or spam-flagged users are denied permission to create or destroy blocks.
- Attempting to unblock a user for whom no block record exists raises `ActiveRecord::RecordNotFound`.
