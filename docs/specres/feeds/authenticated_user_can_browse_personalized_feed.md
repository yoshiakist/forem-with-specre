---
id: "01KJV9M0QR6H05KCHZ72V7A2BZ"
name: "authenticated_user_can_browse_personalized_feed"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stories/feeds_controller.rb`
- `app/models/articles/feeds.rb`
- `app/services/articles/feeds/basic.rb`
- `app/services/articles/feeds/custom.rb`
- `app/services/articles/feeds/large_forem_experimental.rb`
- `app/services/articles/feeds/article_score_calculator_for_user.rb`
- `app/services/articles/feeds/find_featured_story.rb`
- `app/models/feed_config.rb`
- `spec/requests/stories/feeds_spec.rb` (Test)
- `spec/requests/articles/articles_feed_spec.rb` (Test)
- `spec/models/articles/feeds_spec.rb` (Test)
- `spec/services/articles/feeds/basic_spec.rb` (Test)
- `spec/services/articles/feeds/custom_spec.rb` (Test)
- `spec/services/articles/feeds/large_forem_experimental_spec.rb` (Test)
- `spec/services/articles/feeds/article_score_calculator_for_user_spec.rb` (Test)
- `spec/services/articles/feeds/find_featured_story_spec.rb` (Test)
- `spec/models/feed_config_spec.rb` (Test)
- `spec/system/articles/feeds/basic_spec.rb` (Test)
- `spec/system/articles/feeds/large_forem_experimental_spec.rb` (Test)
- `spec/services/articles/feeds_spec.rb` (Test)

## Functional Overview

When a signed-in user requests `GET /stories/feed` without a timeframe or following parameter, the controller calls `signed_in_base_feed`, choosing between `Articles::Feeds::Basic`, `Articles::Feeds::Custom` (with a selected `FeedConfig`), or an experiment-assigned variant via `Articles::Feeds.feed_for`. The selected strategy scores and ranks articles based on the user's relationships (followed users, tags, organizations), experience-level proximity, and comment activity. The `Custom` strategy applies a dynamic SQL scoring expression from `FeedConfig#score_sql` at the database level, with optional weighted shuffling. The response is returned as JSON without edge-cache headers so personalization remains accurate.

## Design Intent

Feed strategy selection is intentionally open to A/B experimentation via `AbExperiment.get_feed_variant_for`, allowing the platform to test `Basic`, `LargeForemExperimental`, and weighted `VariantQuery` strategies without code changes. The `Custom` strategy driven by a `FeedConfig` record supports an evolutionary scoring model where feed weights are mutated slightly (via `create_slightly_modified_clone!`) to explore better configurations over time. Authenticated requests are never edge-cached.

## Key Members

- `FeedsController#signed_in_base_feed` — selects the feed strategy and executes it via `more_comments_minimal_weight_randomized`.
- `feed_strategy` (`Settings::UserExperience`) — platform-wide setting selecting `"basic"`, `"large_forem_experimental"`, or `"configured"` (uses `FeedConfig`).
- `FeedConfig#score_sql` — generates a dynamic SQL scoring expression composed of weighted terms for follow relationships, recency, tag matches, labels, subforems, and randomness.
- `ArticleScoreCalculatorForUser` — encapsulates in-memory scoring of articles by followed tags, users, organizations, experience level, and comments (used by `Basic` and `LargeForemExperimental`).

## Scenarios

### Authenticated user browses a personalized feed

1. A signed-in user requests `GET /stories/feed`.
2. The controller calls `signed_in_base_feed`, choosing `Articles::Feeds::Basic`, `Articles::Feeds::Custom` (with a selected `FeedConfig`), or an experiment-assigned variant via `Articles::Feeds.feed_for`.
3. For `Basic`, articles are initially sorted by hotness score; blocked users' articles are removed and anti-followed tag articles are filtered out; then results are re-ranked in-memory by summing scores for followed tags, followed users, and followed organizations.
4. For `Custom`, a SQL scoring expression from `FeedConfig#score_sql` is applied at the database level and a weighted shuffle is optionally applied.
5. The final ranked list is returned as JSON without edge-cache headers.

## Failures / Exceptions

- Articles authored by users blocked by the current user are excluded before personalization scoring is applied.
- A `Custom` feed with a `nil` `feed_config` or a `nil` user returns an empty array immediately.
