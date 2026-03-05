---
id: "01KHZ6KMGFYFBB8TCE6Q554D1Z"
name: "system_keeps_profile_display_fresh"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/workers/users/bust_profile_details_cache_worker.rb`
- `app/workers/users/bust_profile_identity_cache_worker.rb`
- `app/workers/users/bust_profile_image_cache_worker.rb`
- `spec/workers/users/bust_profile_details_cache_worker_spec.rb` (Test)
- `spec/workers/users/bust_profile_identity_cache_worker_spec.rb` (Test)
- `spec/workers/users/bust_profile_image_cache_worker_spec.rb` (Test)
- `app/services/edge_cache/bust_user.rb`
- `app/workers/users/bust_cache_worker.rb`
- `spec/services/edge_cache/bust_user_spec.rb` (Test)
- `spec/workers/users/bust_cache_worker_spec.rb` (Test)

## Functional Overview

When a user's profile data changes, the system enqueues one or more background workers to invalidate the relevant edge-cache entries so that visitors always see up-to-date information. Three specialized workers handle three distinct cache segments: profile details (general profile record data), profile identity (linked identity/social-account data), and profile image (avatar/photo data). Each worker looks up the user by ID, silently exits if the user no longer exists, and then calls `EdgeCache::PurgeByKey` with the segment-specific cache key and a list of fallback paths to purge.

## Scenarios

### Busting the profile details cache

1. The worker receives a user ID.
2. It looks up the user record.
3. It calls `EdgeCache::PurgeByKey` with the user's `profile_details_record_key` and `profile_cache_bust_paths` as fallback paths, causing the cached profile details to be invalidated at the edge.

### Busting the profile identity cache

1. The worker receives a user ID.
2. It looks up the user record.
3. It calls `EdgeCache::PurgeByKey` with the user's `profile_identity_record_key` and `profile_cache_bust_paths` as fallback paths, invalidating any cached identity/social-account data.

### Busting the profile image cache

1. The worker receives a user ID.
2. It looks up the user record.
3. It calls `EdgeCache::PurgeByKey` with the user's `profile_image_record_key` and `profile_cache_bust_paths` as fallback paths, invalidating any cached avatar or photo data.

### Busting all user profile caches at once

1. `EdgeCache::BustUser` receives a user object.
2. It retrieves all of the user's profile cache keys via `profile_cache_keys` and the fallback paths via `profile_cache_bust_paths`.
3. It calls `EdgeCache::PurgeByKey` once with all keys and fallback paths, invalidating every profile cache segment in a single operation.

### Async user cache busting via worker

1. `Users::BustCacheWorker` receives a user ID.
2. It looks up the user record by that ID.
3. If the user exists, it delegates immediately to `EdgeCache::BustUser`, which handles all cache key purging.
4. If the user no longer exists, the worker exits without performing any purge.

### User not found

1. The worker receives a user ID that does not correspond to any existing user.
2. The lookup returns nothing and the worker exits immediately without calling `EdgeCache::PurgeByKey` and without raising an error.

## Design Intent

Splitting the cache invalidation into three narrow workers (details, identity, image) allows callers to bust only the segment that actually changed, avoiding unnecessary purge calls for unrelated cache segments. The silent no-op on a missing user makes each worker safe to enqueue optimistically without requiring the caller to verify the user still exists at enqueue time.
