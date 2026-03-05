---
id: "01KJ6FPJ10B16C1P2RH854CJ1B"
name: "system_awards_thumbs_up_milestone_badges"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/badges/award_thumbs_up.rb`
- `spec/services/badges/award_thumbs_up_spec.rb` (Test)

## Functional Overview

`Badges::AwardThumbsUp` is a batch service that scans all Article thumbs-up reactions, groups them by the reacting user, and awards cumulative milestone badges (100, 500, 1,000, 5,000, and 10,000 thumbs-up) to every user who has crossed each threshold. The service fetches the badge database IDs up front and aborts the entire run if any milestone badge is missing from the database. For each user whose total thumbs-up count meets or exceeds a threshold, a `BadgeAchievement` record is created; duplicate prevention is delegated to the database-level uniqueness constraint on that model.

## Key Members

- `THUMBS_UP_BADGES` — maps integer milestone thresholds to badge titles: 100, 500, 1,000, 5,000, and 10,000
- `MIN_THRESHOLD` — the smallest threshold (100), used to filter users in the database query so only users with at least one eligible milestone are loaded
- `.call` — entry point; orchestrates fetching badge IDs, querying user counts, and creating `BadgeAchievement` records
- `.get_user_thumbsup_counts` — returns a hash of `user_id => count` for users with at least `MIN_THRESHOLD` thumbs-up reactions on Articles, ordered by count descending
- `.fetch_badge_ids` — queries the `badges` table for all milestone badge titles and returns a hash of `threshold => badge_id`
- `.generate_message(threshold:)` — produces the rewarding context message via `I18n.t("services.badges.thumbs_up", count: threshold)`

## Scenarios

### All milestone badges are missing from the database

1. The service fetches badge IDs for all five milestone titles.
2. One or more badge IDs are not found, leaving `nil` values in the ID map.
3. The service detects the nil and returns immediately without querying reactions or creating any achievements.

### User reaches a single milestone threshold

1. All five milestone badges exist in the database.
2. The service queries thumbs-up reaction counts; a user has a count that meets exactly one threshold (e.g., 100).
3. The service creates one `BadgeAchievement` for that user, linking them to the 100 thumbs-up badge and attaching the generated context message.
4. Users below the minimum threshold receive no badges.

### User crosses multiple milestone thresholds

1. All five milestone badges exist in the database.
2. A user's thumbs-up count meets or exceeds several thresholds (e.g., 10,000 covers all five).
3. The service iterates through every threshold in ascending order and creates a `BadgeAchievement` for each one the user's count satisfies.
4. The user ends up with all applicable milestone badges in a single `.call` run.

### Badge is not awarded a second time

1. A user already has a `BadgeAchievement` for a given milestone badge.
2. The service runs again and the user's count still meets that threshold.
3. The attempt to create a duplicate `BadgeAchievement` is rejected by the database uniqueness constraint; the user's badge count remains unchanged.
