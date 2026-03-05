---
id: "01KJXTKJAC59CZP545HFYJCTGR"
name: "system_renders_homepage_sidebar_widgets"
status: "draft"
---

## Related Files

- `app/views/sidebars/_homepage_content.html.erb`
- `spec/system/homepage/user_visits_homepage_spec.rb` (Test)

## Functional Overview

The homepage sidebar partial (`_homepage_content.html.erb`) is fetched asynchronously via `/sidebars/home` and renders up to three billboard advertisements (first above discussions, second after discussions, third as a sticky element at the bottom). For signed-in users it conditionally shows an active discussions section when the `display_sidebar_active_discussions` setting is enabled. On the root subforem it renders cross-post sections for each discoverable non-root subforem, each listing up to five recently-commented articles sorted by recency and engagement score. On non-root subforems it renders tag-based article lists for each tag configured in `Settings::General.sidebar_tags`, with a special case for the "help" tag that uses `Article.active_help`. The inner content block is fragment-cached with a TTL of 90 seconds for the default timeframe and 180 seconds for explicit timeframe parameters.

## Design Intent

Fragment caching the inner content block reduces database load on high-traffic homepages by avoiding repeated queries for article lists and subforem data on every page load. Fetching the sidebar asynchronously via a dedicated `/sidebars/home` endpoint keeps the initial HTML response fast and allows the cache to be shared across users regardless of sign-in state (the cache key encodes sign-in state and subforem separately). Billboard slots are placed outside the cached fragment so that ad impressions can be controlled independently.

## Key Members

- `@billboards` — array of billboard records fetched by `get_homepage_sidebar_billboards`; positions: first (top), second (mid), third (sticky bottom)
- `@active_discussions` — array of plucked article tuples shown in the active-discussions section when the user is signed in and the setting is enabled
- `Settings::General.display_sidebar_active_discussions` — boolean setting that gates the active discussions section
- `Settings::General.sidebar_tags` — list of tag names rendered as tag-widget sections on non-root subforems
- `is_root_subforem?` — helper that determines whether to show subforem cross-post sections or tag-based sections
- `release_adjusted_cache_key` — helper that builds a cache key incorporating the release version, timeframe, sign-in state, and subforem ID

## Scenarios

### Billboard advertisements are rendered in their designated slots

1. The system fetches billboard records via `get_homepage_sidebar_billboards`.
2. If a first billboard exists it is rendered at the top of the sidebar, above the discussions section.
3. If a second billboard exists it is rendered after the discussions section.
4. If a third billboard exists it is rendered inside a sticky container (`#sticky-billboard`) at the bottom of the sidebar.

### Active discussions section is shown to signed-in users when enabled

1. A signed-in user visits the homepage.
2. `Settings::General.display_sidebar_active_discussions` is `true` and `@active_discussions` contains at least one entry.
3. The system renders the "Active discussions" section (`#active-discussions`) listing each discussion article widget, skipping any item whose title is "[Boost]".

### Active discussions section is hidden when setting is disabled or user is signed out

1. Either the visiting user is not signed in, or `Settings::General.display_sidebar_active_discussions` is `false`.
2. The system does not render the `#active-discussions` section regardless of whether discussion data is available.

### Root subforem shows cross-post sections for discoverable non-root subforems

1. `is_root_subforem?` returns true.
2. For each subforem where `discoverable` is true and `root` is false, the system queries up to five published articles that have at least one comment, meet the minimum home-feed score, and were published within the last week, ordered by recent comment activity and capped engagement score.
3. If articles are found, a card section is rendered showing the subforem's logo, name (linked to its domain), description, and article widgets; "[Boost]"-titled articles are skipped.
4. If no articles qualify for a subforem, that subforem's section is omitted entirely.

### Non-root subforem shows tag-based article lists

1. `is_root_subforem?` returns false.
2. For each tag name in `Settings::General.sidebar_tags`, the system loads the matching tag record.
3. For the "help" tag the system uses `Article.active_help` limited to five articles; for all other tags it uses `active_threads` filtered by that tag, timeframe, and limited to five articles.
4. A card section is rendered for each tag showing the tag name as a link, its short summary, and article widgets; "[Boost]"-titled articles are skipped.

## Failures / Exceptions

- If `@billboards` is empty all three billboard slots are silently omitted; no error is raised.
- If a subforem has no qualifying articles its section is skipped without rendering an empty card.
- The content fragment is cached per `[timeframe, sign-in state, subforem_id]`; stale content may appear for up to 90–180 seconds after articles or settings change.
