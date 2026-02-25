---
id: "01KJ9KBD37APR9VXPVW9CZANV7"
name: "moderator_can_merge_users"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/services/moderator/merge_user.rb`
- `spec/services/moderator/merge_user_spec.rb` (Test)

## Functional Overview

`Moderator::MergeUser` allows an admin to consolidate two user accounts by merging all content, social connections, profile data, and identities from a user to be deleted into a user to be kept. After transferring articles, comments, reactions, follows, mentions, badge achievements, GitHub repos, and social usernames, the service deletes the source user account and triggers a cache bust and async sync for the surviving user.

## Design Intent

The merge is designed as a one-way, destructive operation: the delete-user is fully absorbed into the keep-user and then removed. Identity transfer is guarded to prevent duplicate providers, keeping authentication consistent. Social usernames are only copied when the keep-user does not already have them, avoiding overwrites of existing data.

## Key Members

- `keep_user` — the user account that survives the merge and receives all transferred data
- `admin` — the moderator performing the operation
- `delete_user_id` — ID of the user account to be absorbed and deleted

## Scenarios

### Successful merge

1. An admin invokes the merge with a keep-user and a delete-user ID.
2. The service validates that the two users are not the same account.
3. Auth identities from the delete-user are transferred to the keep-user, provided they have no overlapping providers and the delete-user has at most one identity.
4. All articles, comments, and reactions belonging to the delete-user are reassigned to the keep-user and their counts are updated.
5. Follows initiated by the delete-user and followers of the delete-user are reassigned to the keep-user.
6. Mentions referencing the delete-user are reassigned to the keep-user.
7. GitHub repos and badge achievements are reassigned; badge counts are recalculated.
8. Social usernames (Twitter, GitHub) from the delete-user are copied to the keep-user only if the keep-user does not already have them.
9. If the delete-user has an earlier `created_at`, the keep-user's `created_at` is updated accordingly.
10. The delete-user account is permanently removed, the keep-user's profile timestamps are touched, an async sync worker is enqueued, and the keep-user's public profile cache is busted.

### Badge achievements are transferred

1. The delete-user holds one or more badge achievements.
2. After the merge, all badge achievements are reassigned to the keep-user.
3. The keep-user's `badge_achievements_count` is recalculated to reflect the combined total.

## Failures / Exceptions

- Raises `StandardError` if `keep_user` and `delete_user` are the same account.
- Raises `StandardError` if the delete-user has two or more auth identities (cannot safely transfer multiple providers).
- Raises `StandardError` if both users share at least one auth provider (would create a duplicate identity on the keep-user).
