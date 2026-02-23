---
id: "01KJ41NGKZDC2HQCNEQDKZYTDM"
name: "system_busts_tag_cache_on_changes"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/edge_cache/bust_tag.rb`
- `app/workers/tags/bust_cache_worker.rb`
- `spec/services/edge_cache/bust_tag_spec.rb` (Test)
- `spec/workers/tags/bust_cache_worker_spec.rb` (Test)

## Functional Overview

When a tag changes, the system invalidates its cached representations by purging the tag object itself and busting the edge cache for all URL paths associated with that tag. The `EdgeCache::BustTag` service handles the cache-busting logic directly, while `Tags::BustCacheWorker` acts as the asynchronous entry point that looks up the tag by name and delegates to the service. Together they ensure stale content is not served after tag updates.

## Design Intent

The worker accepts a tag name (a string) rather than a tag object or ID so that it can be safely enqueued without holding a reference to an in-memory object. The service guards against a missing tag with an early return, and the worker does the same after its database lookup, making both layers independently safe to call even when the tag no longer exists.

## Scenarios

### Cache is busted for an existing tag

1. A caller enqueues `Tags::BustCacheWorker` with a tag name.
2. The worker looks up the tag by name in the database.
3. Because the tag exists, the worker delegates to `EdgeCache::BustTag.call` with the tag record.
4. The service calls `purge` on the tag object to clear its ActiveRecord cache.
5. The service then busts the edge cache for `/t/<tag_name>`, `/t/<tag_name>/`, and `/tags`.

### Cache bust is skipped when the tag does not exist

1. A caller enqueues `Tags::BustCacheWorker` with a tag name that has no matching database record.
2. The worker attempts to find the tag by name and receives `nil`.
3. The worker returns early without calling `EdgeCache::BustTag`, leaving the cache untouched.

### Cache bust is skipped when nil is passed to the service directly

1. A caller invokes `EdgeCache::BustTag.call` with `nil` instead of a tag object.
2. The service detects the falsy argument and returns immediately without purging or busting any paths.
