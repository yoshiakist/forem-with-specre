---
id: "01KJXW7NX99QAAKES46SCR9KHK"
name: "system_busts_listing_cache"
status: "draft"
---

## Related Files

- `app/workers/listings/bust_cache_worker.rb`
- `app/models/listing.rb`

## Functional Overview

When a listing changes, the system enqueues a background job — `Listings::BustCacheWorker` — to invalidate the edge cache for that listing. The worker receives the listing's ID, looks up the corresponding `Listing` record, and, if found, delegates to the `EdgeCache::BustListings` service to purge cached responses. The job runs on a high-priority queue with retry logic and deduplication to prevent redundant cache purges during rapid updates.

## Design Intent

Decoupling cache invalidation into a dedicated high-priority Sidekiq worker ensures that edge-cache purges happen asynchronously without blocking the request cycle. Using `until_executing` lock deduplication prevents duplicate purge jobs from queuing when a listing is updated multiple times in quick succession.

## Key Members

- `listing_id` — the ID of the listing whose cache should be invalidated; passed as the sole argument to the worker's `perform` method.

## Scenarios

### Cache is busted for an existing listing

1. A change to a listing triggers a call to enqueue `Listings::BustCacheWorker` with the listing's ID.
2. The worker picks up the job on the high-priority queue.
3. The worker looks up the listing by ID.
4. Because the listing exists, the worker calls `EdgeCache::BustListings` to invalidate all edge-cached responses for that listing.

### Worker receives an ID for a non-existent listing

1. A job is enqueued for a listing ID that no longer exists in the database (e.g., the listing was deleted before the job ran).
2. The worker looks up the listing by ID and finds no record.
3. The worker returns early without calling the cache-busting service; no error is raised.

### Duplicate jobs are deduplicated

1. Multiple updates to the same listing occur in rapid succession, each enqueuing a `Listings::BustCacheWorker` job with the same listing ID.
2. The `until_executing` lock strategy ensures that only one copy of the job executes at a time; subsequent identical jobs are dropped or deferred until the first finishes.
3. The edge cache is busted exactly once per execution window rather than redundantly.
