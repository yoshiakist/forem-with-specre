---
id: "01KJ9K81WPHS5C4RC219RP1DMK"
name: "system_selects_moderators_for_round_robin_notifications"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/queries/users/select_moderators_query.rb`
- `spec/queries/users/select_moderators_query_spec.rb` (Test)

## Functional Overview

When the system needs to select moderators eligible to receive round-robin moderation notifications, it queries for trusted users who have been recently active and have not received a moderation notification too recently. Specifically, the query returns users with the trusted role who have reacted within the past week, whose last moderation notification was sent more than three days ago, and who have opted into round-robin moderation notifications in their notification settings.

## Design Intent

The three-day cooldown on `last_moderation_notification` prevents the same moderator from being flooded with repeated notifications in quick succession. The one-week activity window on `last_reacted_at` ensures that only currently active moderators are selected, avoiding notification fatigue for inactive users. Together these constraints implement a fair, round-robin distribution of moderation work across the active moderator pool.

## Scenarios

### Returns eligible moderators

1. The system queries for users who hold the trusted role.
2. It filters to only those who have reacted within the past week, confirming they are recently active.
3. It further filters to only those whose last moderation notification was sent more than three days ago, ensuring the cooldown has elapsed.
4. It requires that each candidate's notification setting has round-robin moderation notifications enabled.
5. The resulting list contains all trusted users satisfying every condition and excludes anyone who fails even one criterion.

### Returns an empty list when no moderators meet the criteria

1. All trusted users with round-robin notifications enabled either reacted more than a week ago or received a moderation notification within the past three days.
2. The query finds no users that satisfy all conditions simultaneously.
3. The system returns an empty collection.
