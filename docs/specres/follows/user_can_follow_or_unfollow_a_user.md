---
id: "01KJ1X6P8ZE8SXRX8T90FCZH0G"
name: "user_can_follow_or_unfollow_a_user"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/models/follow.rb`
- `app/controllers/follows_controller.rb`
- `app/policies/follow_policy.rb`
- `app/services/follows/check_cached.rb`
- `app/services/follows/delete_cached.rb`
- `app/workers/users/follow_worker.rb`
- `app/javascript/packs/followButtons.js`
- `app/javascript/utilities/sendFollowUser.js`
- `app/javascript/sidebar-widget/SidebarWidget.jsx`
- `app/javascript/sidebar-widget/sidebarUser.jsx`
- `spec/models/follow_spec.rb` (Test)
- `spec/policies/follow_policy_spec.rb` (Test)
- `spec/requests/follows_create_spec.rb` (Test)
- `spec/requests/follows_show_spec.rb` (Test)
- `spec/requests/follows_bulk_show_spec.rb` (Test)
- `spec/services/follows/check_cached_spec.rb` (Test)
- `spec/workers/users/follow_worker_spec.rb` (Test)

## Functional Overview

Authenticated users can follow or unfollow other users (and other followable entities such as tags, organizations, podcasts, and subforems). When a user clicks a follow button, the UI optimistically updates its state and posts to `POST /follows` with the `followable_type`, `followable_id`, and a `verb` of either `"follow"` or `"unfollow"`. The server enforces a daily rate limit on new follows, creates or destroys the `Follow` record accordingly, and returns a plain-text outcome. Follow status is cached per follower and invalidated on unfollow via `Follows::DeleteCached`. On initial page load, buttons fetch their current state individually via `GET /follows/:id` or in bulk via `GET /follows/bulk_show`, and render one of several relationship states: `"false"` (not following), `"true"` (following), `"self"` (own profile), `"follow-back"` (they follow you), or `"mutual"` (both follow each other). A background worker `Users::FollowWorker` also supports programmatic follow creation for `User`, `Tag`, and `Organization` types. After a follow is created, the follower's `last_followed_at` timestamp is updated and, when the follower has badge achievements, an email notification may be enqueued for the followee.

## Design Intent

Follow status is cached with a 20-hour TTL keyed on the follower's `updated_at` timestamp. Because `touch_follower` bumps `updated_at` on every follow save, the cache naturally invalidates when the follower's follow relationships change. On unfollow, `Follows::DeleteCached` eagerly removes the specific cache entry rather than waiting for expiry, ensuring the button state is immediately accurate after an unfollow action.

The bulk status endpoint (`bulk_show`) exists so that pages listing many users (e.g. feeds) can resolve follow states in a single request rather than one request per button.

## Key Members

- `verb` — `"follow"` or `"unfollow"`: controls whether the `create` action follows or unfollows the target
- `followable_type` — the polymorphic type of the target (`"User"`, `"Tag"`, `"Organization"`, `"Podcast"`, `"Subforem"`)
- `subscription_status` — `"all_articles"` or `"none"`: required on every `Follow` record; controls article notification scope
- `explicit_points` / `implicit_points` — numeric weights combined into `points`, used to rank how closely a user follows a given entity

## Scenarios

### User follows another user

1. The current user clicks a follow button on another user's profile or card.
2. The UI immediately updates the button to the "Following" state (optimistic update) and clears the browser store cache.
3. The client posts to `POST /follows` with `followable_type: "User"`, `followable_id`, and `verb: "follow"`.
4. The server checks the daily rate limit; if not exceeded, it creates the `Follow` record, updates the follower's `last_followed_at`, and enqueues an email notification for the followee if they are eligible.
5. The server responds with `{ outcome: "followed" }` and, if applicable, sends a new-follower in-app notification.

### User unfollows another user

1. The current user clicks the "Following" button on a user they already follow.
2. The UI optimistically reverts the button to the "Follow" state.
3. The client posts to `POST /follows` with `verb: "unfollow"`.
4. The server destroys the `Follow` record, marks the prior follower notification as read, and calls `Follows::DeleteCached` to evict the cached follow status.
5. The server responds with `{ outcome: "unfollowed" }`.

### Page loads with follow buttons and fetches current status

1. On page load, `setupFollowFunctionality` scans the DOM for `.follow-action-button` elements.
2. For user and subforem buttons, the client sends a single `GET /follows/bulk_show` request with all relevant IDs and `followable_type`.
3. For other followable types (e.g. tags), status is resolved from locally available user data without a network request.
4. The server responds with a JSON map of IDs to status strings (`"true"`, `"false"`, `"self"`, `"follow-back"`, `"mutual"`).
5. Each button is updated to reflect the correct visual state: outlined "Following", solid "Follow", "Follow Back", or "Edit Profile" for own-profile buttons.

### Mutual follow state is detected

1. User A follows User B and User B follows User A.
2. When either user loads a page containing the other's follow button, the server checks both directions using `Follows::CheckCached`.
3. If both checks return true, the server returns `"mutual"` and the button renders in the "Following" state.
4. If only the other user follows the current user, the server returns `"follow-back"` and the button prompts the user to follow back.

### Rate limit is reached

1. A user attempts to follow more accounts than the daily limit allows.
2. The server returns HTTP 429 with `{ error: "Daily account follow limit reached!" }`.
3. The client surfaces an error modal to the user.

## Failures / Exceptions

- If the follow record already exists when attempting to follow (duplicate), an `ActiveRecord::RecordInvalid` exception is rescued and the outcome is returned as `"already followed"` rather than an error.
- If the current user is not authenticated, `GET /follows/:id` and `GET /follows/bulk_show` return the plain-text string `"not-logged-in"`. A click on a follow button when logged out shows the login modal instead of submitting a request.
- `Users::FollowWorker` silently returns without creating a follow if either the user or the followable record does not exist, or if the `followable_type` is not one of `"Tag"`, `"Organization"`, or `"User"`.
