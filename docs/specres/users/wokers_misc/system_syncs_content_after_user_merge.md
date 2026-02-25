---
id: "01KJ9R3NEXD9DTKEX8J52S80DF"
name: "system_syncs_content_after_user_merge"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/workers/users/merge_sync_worker.rb`
- `spec/workers/users/merge_sync_worker_spec.rb` (Test)

## Functional Overview

After two user accounts are merged, the system re-saves all content that belonged to the absorbed user so that downstream side effects (cache invalidation, score recalculation, and search re-indexing) are triggered via model callbacks. The worker resaves the user's articles, comments, the user's own reading-list reactions, and any reading-list reactions made by other users on the merged user's articles. The job runs on the high-priority queue with up to 10 retries, reflecting that content consistency after a merge is considered time-sensitive.

## Design Intent

The worker deliberately re-triggers existing model callbacks rather than performing targeted cache or index updates directly. This is acknowledged as duplicate-work-heavy but is considered acceptable given that user merges are infrequent. The approach avoids introducing a tight coupling between the merge process and every individual caching or indexing subsystem, deferring optimization until callback dependencies are reduced.

## Scenarios

### Worker is called with a valid user ID

1. The job receives a user ID and looks up the corresponding user record.
2. For each of the user's articles, the system re-saves the record, triggering all model callbacks.
3. For each of the user's comments, the system re-saves the record in the same way.
4. For each reading-list reaction belonging to the user, the system re-saves it.
5. For each reading-list reaction made by any user on the merged user's articles, the system re-saves it.
6. Caches are invalidated, scores are updated, and search documents are re-indexed with the correct user identity as a result of those callbacks.

### Worker is called with a user ID that no longer exists

1. The job receives a user ID that does not match any user record.
2. The system exits early without performing any re-save operations.
