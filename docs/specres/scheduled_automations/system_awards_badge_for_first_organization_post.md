---
id: "01KHZ33RNQX4D71QCX598285TK"
name: "system_awards_badge_for_first_organization_post"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/services/scheduled_automations/first_post_badge_awarder.rb`
- `spec/services/scheduled_automations/first_post_badge_awarder_spec.rb` (Test)

## Functional Overview

The system automatically awards a badge to users who publish their first article under a specific organization. The `FirstPostBadgeAwarder` service finds all published articles under the configured organization since the last automation run (with a 15-minute overlap buffer), groups them by author, determines whether each article is the author's very first post under that organization, and awards a badge to qualifying first-time contributors. The service enforces idempotency by always checking for existing badge achievements regardless of whether the badge allows multiple awards.

## Design Intent

The 15-minute lookback buffer from `last_run_at` prevents missed articles due to timing drift between automation runs. On the first run (when `last_run_at` is nil), the service uses `Time.at(0)` (epoch) to scan all historical articles, ensuring no first-time contributors are overlooked. The idempotency check on existing badge achievements means the automation can safely re-run without creating duplicate awards.

## Key Members

- `organization_id` — the target organization to monitor for first posts (from `action_config`)
- `badge_slug` — identifies the badge to award (from `action_config`)
- `@since_time` — lookback cutoff derived from `last_run_at` minus 15-minute buffer

## Scenarios

### System awards badges to first-time organization contributors

1. Service finds all published articles under the target organization since the lookback cutoff
2. Articles are grouped by author
3. For each author, system identifies their earliest article in the recent set
4. System checks whether the author has any published articles under this organization before the earliest recent article
5. If no earlier articles exist (this is their first post under the org), and the author does not already have the badge, system creates a `BadgeAchievement`
6. The badge achievement includes a congratulatory message referencing the organization name and article title

### System skips users who already have the badge

1. Service finds a first-time contributor under the organization
2. System checks for an existing `BadgeAchievement` for this user and badge
3. If an achievement already exists, the user is skipped (idempotency guarantee)
4. This check applies regardless of whether the badge allows multiple awards

### System only considers the target organization

1. A user has published articles under multiple organizations
2. Service only considers articles under the configured `organization_id`
3. Articles under other organizations do not affect first-post detection for the target org

### System handles subsequent runs with lookback buffer

1. Automation runs with a non-nil `last_run_at`
2. Service looks back from `last_run_at` minus 15 minutes to catch articles that might have been missed
3. Articles published well before the lookback cutoff are not considered in the recent set

### System handles missing configuration

1. If `organization_id` is missing from the action config, service returns a failure result
2. If `badge_slug` is missing, service returns a failure result
3. If the organization or badge does not exist, service returns a failure with a descriptive message

## Failures / Exceptions

- Returns failure if `organization_id` or `badge_slug` is missing from the action config
- Returns failure if the badge with the given slug is not found
- Returns failure if the organization with the given ID is not found
- Returns failure with error details on any unhandled `StandardError`
- Skips banished users without error
- Skips unpublished articles
