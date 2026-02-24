---
id: "01KJ6FNWH1CEFRKAV2VSJC9213"
name: "system_awards_community_wellness_badges"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/badges/award_community_wellness.rb`
- `spec/services/badges/award_community_wellness_spec.rb` (Test)

## Functional Overview

The `Badges::AwardCommunityWellness` service scans the results of the community wellness query and awards streak badges to users who have consistently posted multiple comments per week over a consecutive series of weeks. It evaluates each user's weekly comment history to calculate the longest unbroken streak, then grants a corresponding badge if that streak length matches one of the predefined reward thresholds. A personalized context message is generated and attached to each badge achievement based on whether it is the user's first streak, their longest possible streak, or an intermediate milestone.

## Key Members

- `REWARD_STREAK_WEEKS`: `[1, 2, 4, 8, 16, 24, 32]` — the streak lengths (in weeks) at which a badge is awarded
- Minimum comment count per week: 2 or more comments required for a week to count toward the streak
- Badge slug format: `"<weeks>-week-community-wellness-streak"`

## Scenarios

### User reaches a reward streak milestone

1. The service fetches all users' serialized weekly comment activity from `Comments::CommunityWellnessQuery`.
2. For each user, the service walks their weekly history in order, advancing a running streak counter only when the week index is non-zero, has more than one comment, and is exactly one step ahead of the current streak count.
3. If the final streak length matches one of the reward thresholds (1, 2, 4, 8, 16, 24, or 32 weeks), the service looks up the corresponding badge by its slug.
4. The service creates a `BadgeAchievement` record linking the user to that badge, including a generated context message.

### User does not meet the minimum comment count

1. A user has activity in consecutive weeks but posts only one comment in at least one of those weeks.
2. The streak counter does not advance past weeks with a comment count of one or fewer.
3. If the resulting streak does not match any reward threshold, no badge is awarded for that user.

### User has a gap in their weekly activity

1. A user posts two or more comments in multiple weeks, but those weeks are not consecutive.
2. The streak calculation resets implicitly because a non-consecutive week index breaks the `week_streak + 1 == week` condition.
3. No badge is awarded unless the partial streak before the gap matched a reward threshold.

### Badge or user record cannot be resolved

1. The service attempts to find the user by ID returned from the query.
2. If no matching user exists, processing for that result is skipped.
3. If no badge exists for the computed slug, processing for that user is also skipped.

### Context message generation

1. When a badge is awarded for a 1-week streak, the message uses the "first" locale string.
2. When a badge is awarded for the longest streak (32 weeks), the message uses the "longest" locale string.
3. For all other thresholds, the message uses the "other" locale string, interpolating the week count.
