---
id: "01KHZ32M67KE4Q341R1BPEGPJB"
name: "system_awards_badge_for_quality_article_content"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/services/scheduled_automations/article_content_badge_awarder.rb`
- `spec/services/scheduled_automations/article_content_badge_awarder_spec.rb` (Test)

## Functional Overview

The system automatically awards badges to users who publish quality articles matching configured criteria. The `ArticleContentBadgeAwarder` service searches for recently published articles within a configurable lookback window, filters them by optional keywords (case-insensitive full-text search with ILIKE fallback), applies minimum indexable thresholds, and uses AI (`Ai::BadgeCriteriaAssessor`) to assess whether each article meets custom quality criteria. Qualifying authors receive a badge achievement with a congratulatory message linking to their article. The service respects weekly cooldown periods for badges that allow multiple awards and prevents duplicate awards for single-award badges.

## Design Intent

The lookback window is calculated from the automation's `last_run_at` (plus a 15-minute buffer for overlap) to ensure no articles are missed between runs. The buffer accounts for timing drift in the cron schedule. AI-based quality assessment allows flexible, human-like evaluation of article content against custom criteria without hardcoded rules.

## Key Members

- `badge_slug` — identifies the badge to award (from `action_config`)
- `keywords` — optional list of keywords for article filtering (from `action_config`)
- `criteria` — quality criteria description passed to the AI assessor (from `action_config`)
- `lookback_hours` — configurable lookback window, defaults to 2 hours (from `action_config`)
- `LOOKBACK_BUFFER` — 15-minute overlap buffer added to the lookback window
- `MIN_DAYS_BETWEEN_AWARDS` — 7-day cooldown for badges that allow multiple awards

## Scenarios

### System awards badges to authors of qualifying articles

1. Service finds published articles within the lookback window that match the configured keywords
2. Articles are filtered by minimum indexable threshold (score >= -1, published after minimum date, score >= minimum or featured)
3. For each candidate article, system checks if the author is not banished and has not already been assessed in this run
4. System uses `Ai::BadgeCriteriaAssessor` to evaluate the article against the configured quality criteria
5. If the article qualifies, system creates a `BadgeAchievement` with a congratulatory message referencing the article
6. The author's record is touched to update their cache

### System skips articles that do not match keywords

1. Service searches for articles matching configured keywords via full-text search
2. If full-text search returns no results, system falls back to ILIKE search on title and body
3. Articles that do not match any keyword are excluded from badge consideration

### System respects weekly cooldown for multi-award badges

1. Service checks if the author received the same badge within the last 7 days
2. If a recent award exists, the author is skipped for this run
3. If the last award was more than 7 days ago, the author is eligible for a new award

### System prevents duplicate awards for single-award badges

1. Service checks if the badge allows multiple awards
2. If the badge does not allow multiple awards and the author already has it, the author is skipped entirely

### System handles missing configuration

1. If `badge_slug` is missing from the action config, service returns a failure result
2. If `criteria` is missing from the action config, service returns a failure result
3. If the badge with the configured slug does not exist, service returns a failure with a descriptive message

## Failures / Exceptions

- Returns failure if `badge_slug` or `criteria` is blank in the action config
- Returns failure if the badge with the given slug is not found
- Returns failure with error details on any unhandled `StandardError`
- Skips banished users without error
- Skips users whose articles do not pass AI quality assessment
