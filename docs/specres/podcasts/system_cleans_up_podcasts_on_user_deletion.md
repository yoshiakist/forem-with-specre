---
id: "01KHZ7FPE352W4ESF9QNYKRE34"
name: "system_cleans_up_podcasts_on_user_deletion"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/services/users/delete_podcasts.rb`
- `spec/services/users/delete_podcasts_spec.rb` (Test)

## Functional Overview

When a user is deleted, the system iterates over all of their podcast ownerships, removes each ownership record, and conditionally deletes the associated podcast. A podcast is only deleted when the user being removed is its sole owner; if other owners remain, only the ownership record is removed and the podcast persists. When a podcast is deleted, any roles scoped to that podcast are also removed and the podcast's edge-cache entry is busted.

## Design Intent

Busting the edge cache for deleted podcasts is deferred until after all podcast records have been destroyed, so that the cache invalidation calls are batched rather than interleaved with database deletes.

## Scenarios

### User has no podcast ownerships

1. The system is called with a user who has no `PodcastOwnership` records.
2. No ownerships are iterated, no podcasts are deleted, and no cache busting occurs.

### User is the sole owner of a podcast

1. The system is called with a user who owns a podcast exclusively.
2. The `PodcastOwnership` record linking the user to the podcast is destroyed.
3. All `Role` records scoped to that podcast are destroyed.
4. The podcast record itself is destroyed.
5. After all podcasts are processed, `EdgeCache::BustPodcast` is called with the podcast's path.

### User shares ownership of a podcast with other users

1. The system is called with a user who co-owns a podcast with at least one other user.
2. The `PodcastOwnership` record for the given user is destroyed.
3. Because other `PodcastOwnership` records for the same podcast still exist, the podcast record is left intact and no roles or cache entries are modified.

### Nil user is provided

1. The system is called with a `nil` value instead of a user object.
2. The method returns immediately without performing any database operations or cache busting.
