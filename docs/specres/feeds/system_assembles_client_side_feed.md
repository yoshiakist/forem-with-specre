---
id: "01KJV9M1M80M71Q62GXVK0HWPY"
name: "system_assembles_client_side_feed"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/javascript/articles/Feed.jsx`
- `app/javascript/packs/homePageFeed.jsx`
- `app/javascript/packs/homePage.jsx`
- `app/javascript/articles/index.js`
- `app/views/articles/index.html.erb` (Template)
- `app/javascript/articles/__tests__/Feed.test.jsx` (Test)
- `spec/system/homepage/user_visits_homepage_articles_spec.rb` (Test)
- `spec/system/homepage/user_visits_homepage_spec.rb` (Test)
- `spec/system/homepage/user_visits_homepage_with_announcement_spec.rb` (Test)

## Functional Overview

On the home page, the `Feed` Preact component mounts inside the `#homepage-feed` container (for signed-in users) and fetches the JSON feed endpoint and three billboard advertisement slots in parallel using `Promise.allSettled`. From the feed JSON, the component identifies the first pinned article and the first article with a main image. The list is assembled: first billboard, pinned article, featured image article, podcast episodes (for users who follow podcasts), second billboard (after position 2), remaining articles, and third billboard (after position 7, when enough items exist). Dismissed billboards (tracked in `localStorage`) are excluded. The `renderFeed` callback provided by `homePageFeed.jsx` renders the assembled list using `Article`, `PodcastEpisode`, and billboard HTML components. The `homePageFeed.jsx` module also handles the loading state, empty state (`NoResults`), and featured article analytics.

## Design Intent

The client-side rendering approach allows authenticated users to receive a personalized feed without server-side HTML caching constraints. Billboard advertisements are fetched separately and interleaved at specific positions to balance revenue with reading experience. The `Promise.allSettled` pattern ensures partial failures (e.g., a billboard fetch failing) don't block the entire feed from rendering.

## Key Members

- `Feed` (Preact component) — orchestrates fetching, organizing, and rendering the feed.
- `timeFrame` (string prop on `Feed`) — controls which feed endpoint variant is fetched; an empty string means the default discover feed.
- `renderFeed` (function prop) — callback from `homePageFeed.jsx` that renders the assembled list items.
- `feedConstruct` — maps organized feed items to `Article`, `PodcastEpisode`, or billboard HTML components.
- `insertBillboardsInFeed` — inserts billboard HTML strings at positions 0, 2, and 7 of the organized feed.
- `isDismissed` — checks `localStorage` for previously dismissed billboard SKUs.

## Scenarios

### Client-side feed assembly and display

1. The `Feed` Preact component mounts on the home page and fetches the JSON feed endpoint and three billboard ad slots concurrently using `Promise.allSettled`.
2. From the feed JSON, the component identifies the first pinned article and the first article with a main image.
3. The list is assembled: first billboard, pinned article, featured image article, podcast episodes (for users who follow podcasts), second billboard (after position 2), remaining articles, and third billboard (after position 7, when enough items exist).
4. Dismissed billboards (tracked in `localStorage`) are excluded from the assembled list.
5. The `renderFeed` callback renders the assembled list; fetch errors surface as a danger notice instead of the feed.

## Failures / Exceptions

- If a billboard fetch fails, `Honeybadger.notify` logs the error and the slot is left empty; the feed renders without that billboard.
- If the `Feed` component catches an unexpected error during feed organization, it sets an error state and renders a "There was a problem fetching your feed." danger notice.
