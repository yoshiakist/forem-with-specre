---
id: "01KJ9KAPX00THEMPV2WXQE43HT"
name: "user_can_unblock_another_user"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/user_blocks_controller.rb`
- `app/models/user_block.rb`
- `app/policies/user_block_policy.rb`
- `spec/requests/user_blocks_spec.rb` (Test)
- `spec/models/user_block_spec.rb` (Test)

## Functional Overview

A signed-in user can remove a previously created block against another user by sending a DELETE request with the target user's ID. The controller first short-circuits if the current user is not blocking anyone, then looks up the specific `UserBlock` record and authorizes the action via Pundit. On success the record is destroyed, the blocker's `blocking_others_count` counter is decremented, the blocker's blocked-IDs cache is busted, and a JSON response with `result: "unblocked"` is returned. Only non-spam, non-suspended users are permitted to call this action.

## Scenarios

### Successful unblock

1. A signed-in user sends a DELETE request to `/user_blocks/:blocked_id` with the target user's ID.
2. The system checks that the current user is blocking at least one person.
3. The system finds the matching `UserBlock` record for the current user and the given blocked user ID.
4. The system authorizes the action (the user must not be spam or suspended).
5. The record is destroyed, counters are updated, the cache is invalidated, and the system returns `result: "unblocked"`.

### User is not blocking anyone

1. A signed-in user sends a DELETE request to `/user_blocks/:blocked_id`.
2. The system checks `blocking_others_count` and finds it is zero.
3. Authorization is skipped and the system returns `result: "not-blocking-anyone"` without touching the database.

### Unblock attempted while not signed in

1. An unauthenticated client sends a DELETE request to `/user_blocks/:blocked_id`.
2. The system returns a 401 Unauthorized response with `result: "not-logged-in"`.

### Block record not found

1. A signed-in user sends a DELETE request for a blocked user ID that does not correspond to an existing `UserBlock` record for that blocker.
2. The system raises `ActiveRecord::RecordNotFound` (via `find_by!`), resulting in a 404 response.

## Failures / Exceptions

- If `UserBlock#destroy` fails due to model errors, the system returns a 422 Unprocessable Entity response with the error message in the `error` field.
- A user who is spam or suspended is denied by `UserBlockPolicy#destroy?` and receives a Pundit authorization error.
