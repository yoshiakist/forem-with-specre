---
id: "01KJV9M130S6RWDXS6V4WXKBGM"
name: "user_can_browse_time_filtered_feed"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stories/feeds_controller.rb`
- `app/services/articles/feeds/timeframe.rb`
- `app/services/articles/feeds/latest.rb`
- `app/views/articles/_feed_nav.html.erb` (Template)
- `spec/requests/stories/feeds_spec.rb` (Test)
- `spec/services/articles/feeds/timeframe_spec.rb` (Test)
- `spec/services/articles/feeds/latest_spec.rb` (Test)

## Functional Overview

When a user requests `GET /stories/feed/:timeframe` with a value such as `"week"`, `"month"`, `"year"`, or `"infinity"`, the controller delegates to `Articles::Feeds::Timeframe.call`, which filters published articles to those newer than the matching timeframe boundary, sorted by score descending. When the timeframe is `"latest"`, the controller delegates to `Articles::Feeds::Latest.call`, which returns articles ordered by `published_at DESC`. Both modes are paginated and filtered to a minimum score threshold. The `_feed_nav.html.erb` partial renders navigation links for these temporal filters.

## Design Intent

Timeframe filters provide curated "top" views of content over specific periods, while the latest feed gives a chronological view. No pinned article is prepended when a timeframe parameter is present. Both modes apply a minimum score threshold to exclude low-quality content. These are available to both anonymous and authenticated users and do not involve personalization scoring.

## Key Members

- `FeedsController#timeframe_feed` — delegates to `Articles::Feeds::Timeframe.call`.
- `FeedsController#latest_feed` — delegates to `Articles::Feeds::Latest.call`.
- `Articles::Feeds::Timeframe.call` — filters by `published_at > Timeframe.datetime(timeframe)`, orders by `score DESC`.
- `Articles::Feeds::Latest.call` — orders by `published_at DESC` with minimum score filter.
- `Timeframe::FILTER_TIMEFRAMES` — the set of valid timeframe values (`"week"`, `"month"`, `"year"`, `"infinity"`).
- `Timeframe::LATEST_TIMEFRAME` — the `"latest"` constant.

## Scenarios

### User filters the feed by timeframe

1. A user requests `GET /stories/feed/:timeframe` with a value such as `"week"`, `"month"`, `"year"`, or `"infinity"`.
2. The controller calls `Articles::Feeds::Timeframe.call`, which filters published articles to those newer than the matching timeframe boundary.
3. Results are sorted by score descending, paginated, and filtered to the minimum score threshold.
4. No pinned article is prepended when a timeframe parameter is present.

### User views the latest articles

1. A user requests `GET /stories/feed/latest` (with `timeframe` set to `"latest"`).
2. The controller calls `Articles::Feeds::Latest.call`.
3. Published articles are returned ordered by `published_at DESC`, filtered to a minimum score of -20, and paginated.

## Failures / Exceptions

- An unrecognized timeframe value falls through to the default feed path (not handled by this behavior).
