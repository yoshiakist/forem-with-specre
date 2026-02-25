---
id: "01KJBE9TE08XJE29XJA62XW7VQ"
name: "system_cleans_up_comments_on_user_deletion"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/users/delete_comments.rb`
- `spec/services/users/delete_comments_spec.rb` (Test)

## Functional Overview

When a user is deleted, the system removes all of their comments and associated data. For each comment belonging to the user, the service deletes all reactions on that comment, busts the comment edge cache, removes any notifications tied to the comment, and then deletes the comment record itself. After all comments are processed, the user's own edge cache is also busted to ensure stale content is cleared from CDN or cache layers. If the user has no comments, the service exits early without performing any work.

## Design Intent

The service processes comments one by one using `find_each` to avoid loading all records into memory at once, which is important for users with many comments. Cache busting happens per-comment and also once for the user after the loop, ensuring that both individual comment pages and the user's profile page are invalidated.

## Scenarios

### User has comments — all comments and associated data are removed

1. The service is called with a user who has one or more comments.
2. For each comment, all reactions on the comment are deleted without triggering ActiveRecord callbacks.
3. The edge cache for that comment is busted via `EdgeCache::BustComment`.
4. All notifications associated with the comment are removed.
5. The comment record itself is deleted.
6. After all comments are processed, the edge cache for the user is busted via `EdgeCache::BustUser`.

### User has no comments — service exits early

1. The service is called with a user who has no comments.
2. The service detects that there are no comments and returns immediately without performing any deletions or cache operations.

### Moderation notifications are removed along with comments

1. A trusted user has received a moderation notification linked to one of the deleted user's comments.
2. The service processes the comment and removes all associated notifications, including moderation-type notifications.
3. After the service completes, no notifications remain for that comment.

## Failures / Exceptions

- If the user has no comments, the service returns `nil` immediately without any side effects.
