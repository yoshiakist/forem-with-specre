---
id: "01KHZ34S64MDBEZEVY74YYQ7HM"
name: "system_awards_warm_welcome_badge_for_helpful_comments"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/services/scheduled_automations/warm_welcome_badge_awarder.rb`
- `spec/services/scheduled_automations/warm_welcome_badge_awarder_spec.rb` (Test)
- `app/services/ai/comment_helpfulness_assessor.rb`
- `spec/services/ai/comment_helpfulness_assessor_spec.rb` (Test)

## Functional Overview

The system automatically awards a "warm-welcome" badge to users who leave helpful, substantive comments in the community's Welcome Thread. The `WarmWelcomeBadgeAwarder` service finds the most recent welcome thread (an admin-published article tagged "welcome"), retrieves comments posted within the last 7.5 days, filters out deleted, hidden, low-quality, and spam comments, and uses AI (`Ai::CommentHelpfulnessAssessor`) to determine whether each comment is genuinely helpful. Qualifying users receive a badge achievement with a message encouraging continued participation. The badge can be re-earned weekly with a 6.5-day cooldown between awards.

## Design Intent

The warm welcome badge is designed to incentivize community members to actively welcome newcomers. The automation is non-configurable by design — it always uses the hardcoded `warm-welcome` badge slug and fixed lookback/cooldown constants. The 7.5-day lookback and 6.5-day cooldown create a weekly cadence with built-in overlap to avoid edge-case gaps. Multi-layer quality filtering (score threshold, spam detection, AI helpfulness assessment) ensures only genuinely welcoming comments earn the badge.

## Key Members

- `BADGE_SLUG` — hardcoded as `"warm-welcome"`
- `LOOKBACK_DAYS` — 7.5 days; the window for considering recent comments
- `MIN_DAYS_BETWEEN_AWARDS` — 6.5 days; cooldown between repeat awards to the same user
- `Comment::LOW_QUALITY_THRESHOLD` — score threshold below which comments are automatically excluded

## Scenarios

### System awards badges for helpful welcome thread comments

1. Service finds the most recent welcome thread (preferring the current subforem's thread if available)
2. Service retrieves comments in the welcome thread posted within the last 7.5 days and since the last automation run
3. For each comment, system checks the author is not banished and has not already been assessed in this run
4. System filters out deleted comments and comments hidden by the article author
5. System filters out comments with a score at or below the low-quality threshold
6. System uses `Ai::CommentCheck` to filter out spam comments
7. System uses `Ai::CommentHelpfulnessAssessor` to evaluate whether the comment is helpful and contextual
8. If the comment qualifies, system creates a `BadgeAchievement` with a congratulatory message
9. Each user can receive at most one badge per run, even if they have multiple qualifying comments

### System respects cooldown between repeat awards

1. Service checks if the user received the warm-welcome badge within the last 6.5 days
2. If a recent award exists, the user is skipped for this run
3. If the last award was more than 6.5 days ago, the user is eligible for a new award

### System handles missing welcome thread

1. Service looks for a welcome thread via `Article.cached_admin_published_with("welcome")`
2. If no welcome thread exists, service returns success with zero users awarded (not a failure)

### System handles missing badge

1. Service looks up the badge by slug `"warm-welcome"`
2. If the badge does not exist, service returns a failure result with a descriptive message

### System awards badges for reply comments

1. A user leaves a helpful reply to a newcomer's comment in the welcome thread
2. The reply is assessed the same way as top-level comments
3. If the reply passes all quality filters and AI assessment, the user receives the badge

## Failures / Exceptions

- Returns failure if the badge with slug `"warm-welcome"` is not found
- Returns failure with error details on any unhandled `StandardError`
- Skips deleted comments without error
- Skips comments hidden by the article author without error
- Skips comments below the low-quality score threshold without error
- Skips spam comments (detected by `Ai::CommentCheck`) without error
- Skips banished users without error
