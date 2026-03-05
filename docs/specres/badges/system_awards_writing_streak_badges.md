---
id: "01KJ6FJWX16YC4Y1JXWM0A595S"
name: "system_awards_writing_streak_badges"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/badges/award_streak.rb`
- `app/services/badges/award_four_week_streak.rb`
- `app/services/badges/award_eight_week_streak.rb`
- `app/services/badges/award_sixteen_week_streak.rb`
- `spec/services/badges/award_streak_spec.rb` (Test)
- `spec/services/badges/award_four_week_streak_spec.rb` (Test)
- `spec/services/badges/award_eight_week_streak_spec.rb` (Test)
- `spec/services/badges/award_sixteen_week_streak_spec.rb` (Test)

## Functional Overview

The system awards writing-streak badges to users who publish at least one article per week for a consecutive number of weeks (4, 8, or 16). `Badges::AwardStreak` implements the shared core logic: it filters users who have published a sufficiently high-scoring article within the past week, then verifies that each candidate has at least one published article in every one of the required preceding weekly windows. Qualifying users receive the corresponding streak badge along with a contextual reward message. Three thin facade classes (`AwardFourWeekStreak`, `AwardEightWeekStreak`, `AwardSixteenWeekStreak`) delegate to `AwardStreak` with the appropriate week count.

## Key Members

- `weeks` — the streak length being evaluated (4, 8, or 16); determines which badge slug is looked up and how many consecutive weekly windows must be satisfied.
- `MINIMUM_QUALITY` (`-25`) — score threshold; only articles above this score qualify when identifying the candidate user pool.
- `LONGEST_STREAK_WEEKS` (`16`) — the maximum streak tier; users who reach this milestone receive a distinct "longest streak" reward message instead of the generic one.

## Scenarios

### Four-week streak badge is awarded

1. The scheduler invokes `Badges::AwardFourWeekStreak.call`, which delegates to `Badges::AwardStreak` with `weeks: 4`.
2. The system looks up the badge whose slug is `4-week-streak`; if the badge does not exist, processing stops silently.
3. The system collects all users who published at least one article with a score above -25 within the past week and whose total article count is at least 4.
4. For each candidate user, the system checks whether they published at least one article in each of the four preceding weekly windows (week 1 ago, week 2 ago, week 3 ago, week 4 ago).
5. Users who satisfy all four windows receive a `badge_achievement` record for the four-week-streak badge, along with a contextual reward message.

### Eight-week streak badge is awarded

1. The scheduler invokes `Badges::AwardEightWeekStreak.call`, which delegates to `Badges::AwardStreak` with `weeks: 8`.
2. The same candidate-filtering and per-window verification logic runs for eight consecutive weekly windows.
3. Qualifying users receive the `8-week-streak` badge and the corresponding reward message.

### Sixteen-week streak badge is awarded (longest streak)

1. The scheduler invokes `Badges::AwardSixteenWeekStreak.call`, which delegates to `Badges::AwardStreak` with `weeks: 16`.
2. Candidates must have published in each of the sixteen preceding weekly windows.
3. Qualifying users receive the `16-week-streak` badge with a special "longest streak" message instead of the generic one.

### User with a gap in their streak is not awarded

1. A user has published articles in three out of four required weekly windows but is missing one window.
2. The system counts only three qualifying windows, which is fewer than the required four.
3. No badge achievement is created for that user.

## Failures / Exceptions

- If no badge with the expected slug (e.g., `4-week-streak`) exists in the database, `Badge.id_for_slug` returns `nil` and the method returns early without iterating over any users.
