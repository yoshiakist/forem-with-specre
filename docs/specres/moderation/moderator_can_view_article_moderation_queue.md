---
id: "01KJ16TED32H3YYC9F610VZM5X"
name: "moderator_can_view_article_moderation_queue"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/moderations_controller.rb`
- `app/services/moderations/article_fetcher_service.rb`
- `app/javascript/modCenter/moderationArticles.jsx`
- `app/javascript/modCenter/singleArticle/index.jsx`
- `app/javascript/modCenter/singleArticle/util.js`
- `app/javascript/packs/modCenter.jsx`
- `app/views/moderations/index.html.erb` (Template)
- `app/views/moderations/_mod_sidebar_left.html.erb` (Template)
- `app/views/moderations/_mod_sidebar_right.html.erb` (Template)
- `spec/requests/moderations_spec.rb` (Test)
- `spec/services/moderations/article_fetcher_service_spec.rb` (Test)
- `app/javascript/modCenter/__tests__/moderationArticles.test.jsx` (Test)

## Functional Overview

When a trusted user visits the moderation center (`GET /mod` or `GET /mod/:tag`), the system fetches a filtered list of published articles via `Moderations::ArticleFetcherService` and embeds the result as JSON into the page. The article list is pruned by a minimum score threshold, a configurable lookback window, and — in the default "inbox" feed — by excluding articles the moderator has already reacted to. The moderator can further narrow the queue by feed mode ("inbox" vs "latest"), author membership type ("new", "not_new", or "all"), and optional tag filter. On the client side, the `ModerationArticles` Preact component parses the embedded JSON and renders each entry as a collapsible `SingleArticle` row; clicking a row loads both an article preview iframe and an actions-panel iframe side by side without a full page reload. Non-trusted visitors see an informational page explaining how to become a moderator instead of the queue.

## Design Intent

Articles titled `[Boost]` are filtered out in the service layer to prevent promotional content from appearing in the moderation queue. The inbox feed excludes articles the current moderator has already interacted with (via any reaction), so each moderator sees only unreviewed content. The score-based minimum threshold (`MINIMUM_ARTICLE_SCORE = -5`) keeps very low-quality or spam articles out of the queue without requiring a separate spam list. Tag-specific queue URLs (`/mod/:tag`) allow tag moderators to scope the queue to their area of responsibility, and the sidebar highlights tags the moderator is responsible for or following.

## Key Members

- `feed`: `"inbox"` (default) or `"latest"` — controls whether already-reacted articles are excluded
- `members`: `"new"`, `"not_new"`, or `"all"` — filters by how many articles the author has published
- `tag`: optional tag name — restricts the queue to articles carrying that tag
- `MINIMUM_ARTICLE_SCORE` (`-5`): baseline score below which articles are excluded from all feeds
- `SCORE_MIN` / `SCORE_MAX` (`-10` / `5`): score band applied to the inbox feed to surface borderline content

## Scenarios

### Trusted user views the default inbox queue

1. A trusted user navigates to `GET /mod`.
2. The controller confirms the user has the trusted role; non-trusted or unauthenticated requests receive a not-found response.
3. `Moderations::ArticleFetcherService` is called with `feed: "inbox"` and `members: "all"`.
4. The service builds a base query of published articles within the configured lookback window and above the minimum score threshold, then removes articles the moderator has already reacted to and articles with scores outside the inbox band.
5. Articles titled `[Boost]` are removed from the result set.
6. The serialized JSON is embedded in the page; `ModerationArticles` renders a collapsible row for each article showing the title, tags, author name, and formatted publication date.

### Trusted user filters by tag

1. A trusted user navigates to `GET /mod/:tag`.
2. The tag is looked up (with a one-hour cache); a missing tag raises a not-found error.
3. `ArticleFetcherService` applies `apply_tag_filter`, restricting results to articles tagged with the requested tag.
4. The sidebar left panel highlights the active tag among the moderator's moderated and followed tags.

### Trusted user switches to the "latest" feed or filters by member type

1. The user selects the "Latest" tab or changes the members dropdown on the queue page.
2. The page reloads with `state=latest` and/or a `members` param (`new` or `not_new`).
3. For "latest", the inbox reaction-exclusion filter is skipped; for member filters, the query restricts by `nth_published_by_author` range.
4. The updated article list is rendered in the queue.

### Moderator expands an article row

1. The moderator clicks the summary element of a `SingleArticle` details element.
2. `ModerationArticles.toggleArticle` fires; any previously open article's panel is closed.
3. Two iframes are injected into the article's container: one loading the article path and one loading `<path>/actions_panel/?is_mod_center=true`.
4. The container receives the `opened` CSS class; clicking again removes it and clears the iframe content.

### Non-trusted or unauthenticated user visits /mod

1. A non-trusted or logged-out user requests `GET /mod`.
2. The controller skips Pundit authorization on the index action and returns early without fetching articles.
3. The template renders an informational message describing how to become a trusted user, including links to the code of conduct, trusted-user guide, and tag-moderation guide.
4. If the user is not signed in, an additional notice is shown.

## Failures / Exceptions

- Requesting `GET /mod/:tag` with a tag name that does not exist raises `ActiveRecord::RecordNotFound`.
- Requesting `GET /:username/:slug/mod` or `GET /:username/:slug/actions_panel` without the trusted role or while unauthenticated raises `Pundit::NotAuthorizedError`, which the application maps to a not-found response.
- If the article slug in `load_article` does not match any record, `not_found` is called explicitly.
