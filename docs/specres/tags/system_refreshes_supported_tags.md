---
id: "01KHYCNWVANY5FB7JV8D1ZG2ZZ"
name: "system_refreshes_supported_tags"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/tags/resave_supported_tags_worker.rb
- spec/workers/tags/resave_supported_tags_worker_spec.rb (Test)

## Functional Overview

`Tags::ResaveSupportedTagsWorker` is a scheduled Sidekiq job that periodically re-saves all supported tags and updates subforem scores. Re-saving triggers the Tag model's `before_save` callbacks, which recalculate each tag's hotness score based on recent article engagement. After all tags are processed, every subforem's scores are also refreshed.

## Scenarios

### System periodically refreshes supported tags and subforem scores

1. The worker iterates through all tags where `supported` is true, using `find_each` for memory-efficient batching.
2. Each tag is saved, which triggers the `calculate_hotness_score` callback to recompute the tag's popularity metric based on articles from the last 7 days.
3. The `updated_at` timestamp is refreshed on each tag.
4. After all supported tags are re-saved, the worker iterates through all subforems and calls `update_scores!` on each to refresh their aggregate metrics.
