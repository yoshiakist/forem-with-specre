---
id: "01KJBE9J7SBEYP8CE63NTF4TJQ"
name: "system_cleans_up_articles_on_user_deletion"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/users/delete_articles.rb`
- `spec/services/users/delete_articles_spec.rb` (Test)

## Functional Overview

When a user is deleted, the system removes all articles authored by that user along with their associated data. For each article, it first deletes all reactions on the article, then iterates through each comment to delete comment reactions, bust the comment and commenter edge caches, and delete the comment record. Any discussion lock attached to the article is also removed before the article itself is deleted and purged. After all deletions are complete, the edge cache is busted for each removed article using virtual (in-memory) copies of the article records created before deletion.

## Design Intent

Virtual article copies are captured before deletion begins so that the data needed to bust edge caches (such as slugs and paths) remains available after the database records are removed. This avoids attempting to reload records that no longer exist when busting the CDN cache at the end of the operation.

## Scenarios

### User has no articles

1. The system is called with a user who has no articles.
2. The service detects that the user's article list is blank and returns immediately without performing any operations.

### User has articles with no comments or discussion locks

1. The system is called with a user who has one or more articles.
2. Virtual copies of all articles are created in memory before any deletion.
3. For each article, its reactions are deleted.
4. The article and its purge job are dispatched.
5. After all articles are deleted, the edge cache is busted for each article using the virtual copies.

### User has articles with comments

1. The system is called with a user whose articles have comments from other users.
2. Virtual copies of all articles are captured in memory.
3. For each article, reactions on the article are deleted.
4. For each comment on the article, the comment's reactions are deleted, the comment and commenter edge caches are busted, and the comment record is deleted.
5. The article is deleted and purged.
6. After all deletions, the edge cache is busted for each article using the virtual copies.

### User has articles with discussion locks

1. The system is called with a user whose articles have associated discussion locks.
2. For each article that has a discussion lock, the lock is deleted before the article is removed.
3. The article is then deleted and purged.
4. Article edge caches are busted using the pre-captured virtual copies.
