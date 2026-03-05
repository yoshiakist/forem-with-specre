---
id: "01KJ5DKHGNERDZH7ABTB9SE6E2"
name: "system_busts_comment_cache"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/workers/comments/bust_cache_worker.rb`
- `app/models/comment.rb`
- `spec/workers/comments/bust_cache_worker_spec.rb` (Test)

## Functional Overview

When a comment is saved or destroyed, the system invalidates cached representations of both the comment and its parent commentable resource. Cache busting occurs in two phases: a synchronous phase that runs inline during the save (touching timestamps and purging the commentable immediately), and an asynchronous phase that enqueues `Comments::BustCacheWorker` to purge both the comment and its commentable in a background job. On destroy, the worker is invoked synchronously to ensure caches are cleared before the record is gone. If the comment cannot be found or has no commentable, the worker exits without error.

## Design Intent

The two-phase approach (synchronous then asynchronous) ensures that the commentable's cache is cleared immediately so subsequent requests do not serve stale content, while offloading the potentially slower purge operations to a background queue. Guarding on the existence of both the comment record and its commentable prevents the worker from raising on orphaned or already-deleted records.

## Scenarios

### Asynchronous cache bust after comment save

1. A comment is saved, triggering an `after_save` callback.
2. The system enqueues `Comments::BustCacheWorker` with the comment's ID on the high-priority queue.
3. The worker looks up the comment by ID.
4. The worker purges the cached representation of the comment.
5. The worker purges the cached representation of the commentable resource.

### Synchronous cache bust on save

1. A comment is saved, triggering the synchronous `after_save` callback.
2. If the commentable responds to `last_comment_at`, the system touches that timestamp.
3. The system touches `last_comment_at` on the comment's author.
4. The commentable's cache is purged immediately.
5. The root comment (or the comment itself if it is the root) is touched to expire its fragment cache.

### Cache bust on comment destroy

1. A comment is about to be destroyed.
2. The system touches `last_comment_at` on the commentable if applicable.
3. All ancestor comments have their `updated_at` set to the current time.
4. `Comments::BustCacheWorker` is performed synchronously to purge the comment and commentable caches before the record is deleted.

### Worker skips purge when commentable is absent

1. The worker is called with a comment ID whose comment record exists but has no commentable.
2. The worker detects the missing commentable and returns early without calling purge on either the comment or the commentable.

### Worker skips purge when comment record is not found

1. The worker is called with an ID that does not match any comment (e.g., already deleted or nil).
2. The worker returns early without raising an error or performing any purge.
