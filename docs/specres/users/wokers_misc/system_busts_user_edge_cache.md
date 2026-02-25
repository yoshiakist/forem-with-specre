---
id: "01KJ9R2ZDH9HJZX26S04MK1YNZ"
name: "system_busts_user_edge_cache"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/workers/users/bust_cache_worker.rb`
- `spec/workers/users/bust_cache_worker_spec.rb` (Test)

## Functional Overview

`Users::BustCacheWorker` is a background job that invalidates the edge cache for a given user. When enqueued with a user ID, the worker looks up the user record and, if found, delegates to `EdgeCache::BustUser` to perform the actual cache-busting. If no user exists for the given ID, the worker exits early without taking any action. The worker inherits from `BustCacheBaseWorker`, which provides the Sidekiq worker configuration.

## Scenarios

### Cache is successfully busted for an existing user

1. The job is enqueued with a valid user ID.
2. The worker looks up the user by that ID and finds a matching record.
3. The worker calls `EdgeCache::BustUser` with the user record to invalidate the edge cache.

### Worker does nothing when the user does not exist

1. The job is enqueued with a user ID that no longer exists in the database.
2. The worker attempts to look up the user but finds no matching record.
3. The worker returns early without calling `EdgeCache::BustUser`.

## Failures / Exceptions

- If the user record has been deleted between enqueue time and execution time, the worker silently no-ops, preventing errors from stale job arguments.
