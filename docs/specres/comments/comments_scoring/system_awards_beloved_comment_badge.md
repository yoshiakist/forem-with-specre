---
id: "01KJ44ESWEHQ6F18H90M3CCGNA"
name: "system_awards_beloved_comment_badge"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/badges/award_beloved_comment.rb`
- `spec/services/badges/award_beloved_comment_spec.rb` (Test)

## Functional Overview

`Badges::AwardBelovedComment` is a service that scans all comments and awards the "beloved-comment" badge to the author of any comment that has accumulated at least a configurable number of public reactions (defaulting to 25). For each qualifying comment it creates a `BadgeAchievement` record that includes a localized message with a direct link to the comment, and then touches the comment's author record to update cache timestamps. If the badge does not exist in the system the service exits immediately without doing any work.

## Key Members

- `comment_count` — minimum number of public reactions a comment must have to qualify for the badge. Defaults to 25 when called via the class-level `call` entry point.

## Scenarios

### Badge does not exist in the system

1. The caller invokes `Badges::AwardBelovedComment.call`.
2. The service looks up the badge ID for the slug `beloved-comment` via `Badge.id_for_slug`.
3. No matching badge is found, so the service returns immediately without querying comments or creating any achievements.

### Comment meets the reaction threshold

1. The caller invokes `Badges::AwardBelovedComment.call` (or passes a custom `comment_count`).
2. The service resolves the `beloved-comment` badge ID.
3. The service queries all comments whose `public_reactions_count` is greater than or equal to `comment_count`, eagerly loading each comment's author.
4. For each qualifying comment the service creates a `BadgeAchievement` linking the comment's author to the badge, with a localized rewarding message that includes a URL to the comment.
5. If the `BadgeAchievement` record is valid, the author's record is touched to refresh cache timestamps.

### Comment does not meet the reaction threshold

1. The caller invokes `Badges::AwardBelovedComment.call`.
2. The service resolves the `beloved-comment` badge ID successfully.
3. The service queries comments with `public_reactions_count` at or above the threshold; no comments qualify.
4. No `BadgeAchievement` records are created and no user records are touched.

### Custom reaction threshold provided

1. The caller invokes `Badges::AwardBelovedComment.call(comment_count)` with a non-default integer.
2. The service uses that integer instead of the default 25 as the minimum threshold when querying comments.
3. Otherwise the awarding logic proceeds identically to the standard flow.
