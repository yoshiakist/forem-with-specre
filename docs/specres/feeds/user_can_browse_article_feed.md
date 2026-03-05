---
id: "01KJ246ARS7Y65PKK7T8V3CZFQ"
name: "user_can_browse_article_feed"
status: "deprecated"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/stories/feeds_controller.rb`
- `app/models/articles/feeds.rb`
- `app/services/articles/feeds/basic.rb`
- `app/services/articles/feeds/custom.rb`
- `app/services/articles/feeds/large_forem_experimental.rb`
- `app/services/articles/feeds/article_score_calculator_for_user.rb`
- `app/services/articles/feeds/find_featured_story.rb`
- `app/services/articles/feeds/latest.rb`
- `app/services/articles/feeds/timeframe.rb`
- `app/models/feed_config.rb`
- `app/javascript/articles/Feed.jsx`
- `app/javascript/packs/homePageFeed.jsx`
- `app/javascript/articles/index.js`
- `app/views/stories/_main_stories_feed.html.erb` (Template)
- `app/views/articles/_feed_nav.html.erb` (Template)
- `app/views/articles/index.html.erb` (Template)
- `spec/requests/stories/feeds_spec.rb` (Test)
- `spec/requests/articles/articles_feed_spec.rb` (Test)
- `spec/models/articles/feeds_spec.rb` (Test)
- `spec/services/articles/feeds/basic_spec.rb` (Test)
- `spec/services/articles/feeds/custom_spec.rb` (Test)
- `spec/services/articles/feeds/large_forem_experimental_spec.rb` (Test)
- `spec/services/articles/feeds/article_score_calculator_for_user_spec.rb` (Test)
- `spec/services/articles/feeds/find_featured_story_spec.rb` (Test)
- `spec/services/articles/feeds/latest_spec.rb` (Test)
- `spec/services/articles/feeds/timeframe_spec.rb` (Test)
- `spec/models/feed_config_spec.rb` (Test)
- `spec/system/articles/feeds/basic_spec.rb` (Test)
- `spec/system/articles/feeds/large_forem_experimental_spec.rb` (Test)
- `app/javascript/articles/__tests__/Feed.test.jsx` (Test)
- `spec/services/articles/feeds_spec.rb` (Test)
- `app/queries/homepage/articles_query.rb`
- `app/serializers/homepage/article_serializer.rb`
- `app/services/homepage/fetch_articles.rb`
- `spec/queries/homepage/articles_query_spec.rb` (Test)
- `spec/serializers/homepage/article_serializer_spec.rb` (Test)
- `spec/services/homepage/fetch_articles_spec.rb` (Test)
- `spec/system/homepage/user_visits_homepage_articles_spec.rb` (Test)
- `app/queries/articles/active_threads_query.rb`
- `app/views/articles/_sidebar_additional.html.erb` (Template)
- `app/views/articles/_sidebar.html.erb` (Template)
- `spec/queries/articles/active_threads_query_spec.rb` (Test)

## Functional Overview

When a user visits the home page, the browser fetches a paginated JSON feed from `GET /stories/feed` (handled by `Stories::FeedsController#show`). The controller selects the appropriate feed strategy based on the user's authentication state, the requested timeframe, and the configured `feed_strategy` setting. Anonymous users receive a globally hot or basic feed with edge-cache headers applied; authenticated users receive a personalized feed ranked by a multi-factor relevancy score that weights followed users, tags, and organizations, experience-level proximity, and comment activity. Specialized modes include a timeframe-filtered feed (week, month, year, infinity), a latest-articles feed sorted by publication date, and a following feed restricted to authors or organizations the user follows. On the client side, the `Feed` Preact component fetches the JSON endpoint and three billboard advertisement slots in parallel, then organizes the results into an ordered list of pinned articles, a featured image article, podcast episodes, regular articles, and interleaved billboard HTML, before delegating rendering to the `renderFeed` callback provided by `homePageFeed.jsx`.

## Design Intent

Feed strategy selection is intentionally open to A/B experimentation via `AbExperiment.get_feed_variant_for`, allowing the platform to test `Basic`, `LargeForemExperimental`, and weighted `VariantQuery` strategies without code changes. The `Custom` strategy driven by a `FeedConfig` record supports an evolutionary scoring model where feed weights are mutated slightly to explore better configurations over time. Anonymous users receive a 60-second edge-cache TTL to reduce database load, while authenticated requests are never edge-cached so personalization remains accurate.

## Key Members

- `timeFrame` (string prop on `Feed`) — controls which feed endpoint variant is fetched; an empty string means the default discover feed.
- `feed_strategy` (`Settings::UserExperience`) — platform-wide setting selecting `"basic"`, `"large_forem_experimental"`, or `"configured"` (uses `FeedConfig`).
- `FeedConfig#score_sql` — generates a dynamic SQL scoring expression composed of weighted terms for follow relationships, recency, tag matches, labels, subforems, and randomness.

## Scenarios

### Anonymous user browses the default feed

1. A visitor requests `GET /stories/feed` without authentication credentials.
2. The controller selects the signed-out strategy: `Articles::Feeds::Basic` (if `feed_strategy` is `"basic"`) or `Articles::Feeds.feed_for` for other strategies.
3. Articles are fetched ordered by hotness score, filtered to meet the minimum home-feed score threshold, and scoped to the current subforem.
4. The response is serialized as JSON and decorated via `ArticleDecorator`.
5. Edge-cache headers (`Cache-Control`, `Surrogate-Control`, `X-Accel-Expires`) are set with a 60-second TTL.

### Authenticated user browses a personalized feed

1. A signed-in user requests `GET /stories/feed`.
2. The controller calls `signed_in_base_feed`, choosing `Articles::Feeds::Basic`, `Articles::Feeds::Custom` (with a selected `FeedConfig`), or an experiment-assigned variant via `Articles::Feeds.feed_for`.
3. For `Basic`, articles are initially sorted by hotness score; blocked users' articles are removed and anti-followed tag articles are filtered out; then results are re-ranked in-memory by summing scores for followed tags, followed users, and followed organizations.
4. For `Custom`, a SQL scoring expression from `FeedConfig#score_sql` is applied at the database level and a weighted shuffle is optionally applied.
5. The final ranked list is returned as JSON without edge-cache headers.

### User filters the feed by timeframe

1. A user requests `GET /stories/feed/:timeframe` with a value such as `"week"`, `"month"`, `"year"`, or `"infinity"`.
2. The controller calls `Articles::Feeds::Timeframe.call`, which filters published articles to those newer than the matching timeframe boundary.
3. Results are sorted by score descending, paginated, and filtered to the minimum score threshold.
4. No pinned article is prepended when a timeframe parameter is present.

### Authenticated user browses a following feed

1. A signed-in user requests `GET /stories/feed` with `type_of=following`.
2. The controller resolves followed user IDs and organization IDs from the user's activity store or cached following lists.
3. Articles by those users or organizations with a score above -10 are returned, ordered by `published_at DESC` (latest) or `hotness_score DESC` (relevant), paginated 25 per page.
4. If the user is not authenticated, the request falls through to the standard signed-out feed.

### Client-side feed assembly and display

1. The `Feed` Preact component mounts on the home page and fetches the JSON feed endpoint and three billboard ad slots concurrently using `Promise.allSettled`.
2. From the feed JSON, the component identifies the first pinned article and the first article with a main image.
3. The list is assembled: first billboard, pinned article, featured image article, podcast episodes (for users who follow podcasts), second billboard (after position 2), remaining articles, and third billboard (after position 7, when enough items exist).
4. Dismissed billboards (tracked in `localStorage`) are excluded from the assembled list.
5. The `renderFeed` callback renders the assembled list; fetch errors surface as a danger notice instead of the feed.

## Failures / Exceptions

- If a billboard fetch fails, `Honeybadger.notify` logs the error and the slot is left empty; the feed renders without that billboard.
- If the `Feed` component catches an unexpected error during feed organization, it sets an error state and renders a "There was a problem fetching your feed." danger notice.
- Articles authored by users blocked by the current user are excluded before personalization scoring is applied.
- A `Custom` feed with a `nil` `feed_config` or a `nil` user returns an empty array immediately.
