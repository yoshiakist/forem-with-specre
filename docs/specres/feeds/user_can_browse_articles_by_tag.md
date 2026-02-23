---
id: "01KJ2472X584A2R8VP2QAC7V40"
name: "user_can_browse_articles_by_tag"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/stories/tagged_articles_controller.rb`
- `app/services/articles/feeds/tag.rb`
- `app/views/stories/tagged_articles/_main_feed.html.erb` (Template)
- `app/views/stories/tagged_articles/index.html.erb` (Template)
- `app/views/stories/tagged_articles/_meta.html.erb` (Template)
- `app/views/stories/tagged_articles/_sidebar.html.erb` (Template)
- `app/views/stories/tagged_articles/_sidebar_additional.html.erb` (Template)
- `spec/services/articles/feeds/tag_spec.rb` (Test)
- `spec/requests/stories/tagged_articles_spec.rb` (Test)
- `spec/system/articles/user_visits_articles_by_tag_spec.rb` (Test)

## Functional Overview

When a user navigates to a tag page (e.g., `/t/ruby`), the system looks up the tag by name and returns a paginated, filtered feed of published articles associated with that tag. If the tag is an alias, the user is redirected permanently to the canonical tag. If the tag has no established presence (neither explicitly supported nor having any published articles), the page returns a 404. The feed respects approval requirements for restricted tags, applies timeframe filters when requested, and adjusts the number of articles returned based on whether the visitor is signed in. Surrogate keys are set for CDN cache invalidation, and the response is cached aggressively with stale-while-revalidate and stale-if-error headers.

## Design Intent

The `established?` check prevents empty tag pages from being served to users while still allowing supported tags (e.g., officially recognized tags) to exist before any articles are published under them. Separating the article count query from the feed query allows the article count to be cached independently (72-hour TTL) without affecting the live feed. Page 1 for signed-out users is constrained to recent articles (last 3 months) so the database can use an index on `published_at` before sorting by `hotness_score`, avoiding full-table scans on high-volume tags.

## Key Members

- `SIGNED_OUT_RECORD_COUNT` — fixed number of articles (15) returned per page for unauthenticated visitors; signed-in users receive 5 per page
- `number_of_articles` — per-page limit passed down to `Articles::Feeds::Tag.call`
- `page` — current page number, derived from `params[:page]`, defaults to 1

## Scenarios

### Tag alias redirect

1. User requests a tag page whose `alias_for` field is set.
2. The system issues a permanent redirect to the canonical tag URL (`/t/<alias_for>`).
3. No articles are fetched or rendered.

### Browsing a tag feed (default timeframe)

1. User requests `/t/<tag_name>` without a timeframe parameter.
2. The system looks up the tag by the lowercased name parameter; returns 404 if not found.
3. The system verifies the tag is established (supported or has published articles); returns 404 otherwise.
4. For signed-out users on page 1, articles are constrained to the last 3 months and ordered by `hotness_score` descending above the home feed minimum score.
5. The rendered feed delegates to the `articles/single_story` partial for each decorated article.

### Browsing with a specific timeframe filter

1. User requests `/t/<tag_name>?timeframe=<filter>` where `<filter>` is one of `Timeframe::FILTER_TIMEFRAMES`.
2. The system fetches articles published after the corresponding datetime and orders them by score descending.
3. If the timeframe is `Timeframe::LATEST_TIMEFRAME`, articles are ordered by `published_at` descending instead.

### Browsing a restricted (approval-required) tag

1. User requests a tag page where the tag has `requires_approval?` set.
2. The article count shown is the live count of approved, published, subforem-scoped articles for that tag (not cached).
3. The feed is additionally filtered to approved articles only before rendering.

### Signed-in user sees moderators

1. A signed-in user requests any tag page.
2. The system fetches users with the `tag_moderator` role for that tag, ordered by badge achievement count descending, and exposes them for display.
3. The signed-in user receives 5 articles per page instead of 15.

## Failures / Exceptions

- If the tag name does not exist in the database, `not_found` is called and a 404 response is returned.
- If the tag exists but is not established (not supported and has no published articles in the subforem), `not_found` is called.
- `ArgumentError` raised during request processing is rescued and results in a `bad_request` (400) response.
