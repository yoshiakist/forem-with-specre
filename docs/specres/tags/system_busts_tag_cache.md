---
id: "01KHYCN1D8NN3GXYBG17C9P3XV"
name: "system_busts_tag_cache"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/tags/bust_cache_worker.rb
- spec/workers/tags/bust_cache_worker_spec.rb (Test)

## Functional Overview

`Tags::BustCacheWorker` is a high-priority Sidekiq job that invalidates edge cache entries for a tag whenever its data changes. It is triggered by the Tag model's `after_commit` callback and delegates the actual cache purging to `EdgeCache::BustTag`.

## Scenarios

### System invalidates edge cache for a changed tag

1. After a tag is committed to the database, the Tag model enqueues a `Tags::BustCacheWorker` job with the tag's name.
2. The worker looks up the tag by name.
3. If the tag exists, the worker calls `EdgeCache::BustTag` to purge cached pages associated with the tag.
4. If the tag does not exist (e.g., it was deleted between enqueue and execution), the worker exits silently without calling the cache buster.
