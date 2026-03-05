---
id: "01KJV9KZR85C73CRV2F1MZ7RN8"
name: "anonymous_user_can_browse_default_feed"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stories/feeds_controller.rb`
- `app/models/articles/feeds.rb`
- `app/services/articles/feeds/basic.rb`
- `app/services/articles/feeds/large_forem_experimental.rb`
- `app/services/articles/feeds/article_score_calculator_for_user.rb`
- `app/services/articles/feeds/find_featured_story.rb`
- `app/views/stories/_main_stories_feed.html.erb` (Template)
- `app/views/articles/index.html.erb` (Template)
- `spec/requests/stories/feeds_spec.rb` (Test)
- `spec/requests/articles/articles_feed_spec.rb` (Test)
- `spec/models/articles/feeds_spec.rb` (Test)
- `spec/services/articles/feeds/basic_spec.rb` (Test)
- `spec/services/articles/feeds/large_forem_experimental_spec.rb` (Test)
- `spec/services/articles/feeds/article_score_calculator_for_user_spec.rb` (Test)
- `spec/services/articles/feeds/find_featured_story_spec.rb` (Test)
- `spec/system/articles/feeds/basic_spec.rb` (Test)
- `spec/system/articles/feeds/large_forem_experimental_spec.rb` (Test)
- `spec/services/articles/feeds_spec.rb` (Test)

## Functional Overview

When an unauthenticated visitor requests `GET /stories/feed`, the controller selects the signed-out strategy: `Articles::Feeds::Basic` (when `feed_strategy` is `"basic"`) or the experiment-assigned variant via `Articles::Feeds.feed_for`. Articles are fetched ordered by hotness score, filtered to meet the minimum home-feed score threshold, and scoped to the current subforem. The response is serialized as JSON via `ArticleDecorator`. Edge-cache headers (`Cache-Control`, `Surrogate-Control`, `X-Accel-Expires`) are set with a 60-second TTL. For server-rendered anonymous visitors, `_main_stories_feed.html.erb` renders the feed with interleaved billboard ads.

## Design Intent

Anonymous users receive a globally hot feed without personalization. A 60-second edge-cache TTL reduces database load for the most common visitor profile. No pinned article is prepended when a timeframe parameter is present. The `LargeForemExperimental` strategy's signed-out path returns articles ordered by `hotness_score DESC` with pagination, while `Basic` returns articles ordered by `hotness_score DESC` with a minimum score threshold.

## Key Members

- `FeedsController#signed_out_base_feed` — selects `Basic` or experiment variant and executes the query with Datadog tracing.
- `FeedsController#add_pinned_article` — prepends a platform-pinned article to the feed if present and not already included.
- `Articles::Feeds::Basic#default_home_feed` — returns articles ordered by hotness score; returns directly without personalization scoring when `@user` is nil.
- `Articles::Feeds::LargeForemExperimental#globally_hot_articles` — signed-out path returns paginated articles by hotness score.

## Scenarios

### Anonymous user browses the default feed

1. A visitor requests `GET /stories/feed` without authentication credentials.
2. The controller selects the signed-out strategy: `Articles::Feeds::Basic` (if `feed_strategy` is `"basic"`) or `Articles::Feeds.feed_for` for other strategies.
3. Articles are fetched ordered by hotness score, filtered to meet the minimum home-feed score threshold, and scoped to the current subforem.
4. The response is serialized as JSON and decorated via `ArticleDecorator`.
5. Edge-cache headers (`Cache-Control`, `Surrogate-Control`, `X-Accel-Expires`) are set with a 60-second TTL.

## Failures / Exceptions

- Articles authored by blocked users are not filtered for anonymous users (no blocking context exists).
- A platform-pinned article that has been removed or is nil is silently skipped.
