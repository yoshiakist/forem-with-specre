---
id: "01KJ41JP9GAVXCTXZZXZ1NPNP8"
name: "system_awards_badge_for_top_tag_posts"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/badges/award_tag.rb`
- `spec/services/badges/award_tag_spec.rb` (Test)

## Functional Overview

`Badges::AwardTag` is a service that periodically awards a badge to the author of the highest-scoring article tagged with each badge-eligible tag. For every tag that has an associated badge, the system identifies the top-scoring published article from the past seven days that was not authored by any previous winner of that tag's badge. If such an article exists, the system creates a `BadgeAchievement` for the article's author, attaching a personalized congratulatory message with links to the winning tag and article. The minimum score threshold for eligibility is configurable via `Settings::UserExperience.award_tag_minimum_score`.

## Design Intent

Each user can only win a given tag badge once. By collecting all prior winners' user IDs up front and excluding their articles from eligibility, the system ensures the badge circulates to new contributors over time rather than being retained by a single high-scorer. The 7.5-day lookback window (rather than exactly 7 days) provides a small buffer to avoid edge-case timing issues when the job runs slightly late.

## Scenarios

### Badge awarded to the top-scoring eligible article author

1. The service iterates over all tags that have an associated badge.
2. For each tag, it collects the user IDs of everyone who has already received that tag's badge.
3. It finds the highest-scoring published article tagged with the current tag that was published within the past seven days and whose author has not previously won the badge. The article's score must exceed the configured minimum score threshold.
4. If such an article is found, the system creates a `BadgeAchievement` for the article's author, recording the badge ID and a congratulatory message containing links to the tag page and the winning article.
5. The author's record is touched to reflect the update.

### No badge awarded when no qualifying article exists

1. The service evaluates a tag's articles but none meet all eligibility criteria (sufficient score, correct tag, published within the past seven days, and authored by a non-previous-winner).
2. The service skips that tag without creating any `BadgeAchievement`.

### Previous winners are excluded from winning again

1. A user who previously won a badge for a given tag has their user ID recorded in `BadgeAchievement`.
2. On subsequent runs, that user's articles are excluded from consideration for the same tag's badge, allowing the next-highest-scoring eligible author to win.

### Configurable minimum score threshold

1. `Settings::UserExperience.award_tag_minimum_score` controls the score threshold for article eligibility.
2. Only articles whose score strictly exceeds this threshold are considered for the badge.

## Failures / Exceptions

- If a tag has no badge associated (`badge_id` is nil), it is skipped entirely.
- If the winning article's author already has the badge (race condition or duplicate call), the `BadgeAchievement` creation may fail silently; the author's record is only touched if the achievement was successfully persisted.
