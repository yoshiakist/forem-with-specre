---
id: "01KJ41WT9YWTD6G9MHPTQW0EFA"
name: "user_can_discover_tags"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/tags_controller.rb`
- `app/views/tags/index.html.erb` (Template)
- `app/views/layouts/_sidebar_tags.html.erb` (Template)
- `app/views/sitemaps/tags.xml.erb` (Template)
- `spec/requests/tags_spec.rb` (Test)

## Functional Overview

Users can discover tags through three distinct endpoints. The `GET /tags` page renders an HTML view listing all tags from the current subforem, ordered by hotness score, with a search field that filters tags by name. The `GET /tags/bulk` endpoint returns a JSON list of tags filterable by arrays of tag IDs or tag names, with pagination support. The `GET /tags/suggest` endpoint returns a lightweight JSON list of the top 100 tags by hotness score for use in autocomplete or suggestion UIs. Tags with an `alias_for` value are excluded from the `index` listing because the private `tags` helper calls `.direct`, which filters out alias tags. All three discovery actions skip authorization and are accessible without authentication.

## Design Intent

The three endpoints serve different client needs: the HTML index page is for human browsing, `bulk` is for batch data fetching by client-side code (e.g., resolving tag metadata from stored IDs or names), and `suggest` is for lightweight suggestion dropdowns. Separating them avoids building a single overloaded endpoint. Cache control headers are applied only to the `index` action to enable HTTP caching for the public page without affecting the JSON endpoints.

## Key Members

- `INDEX_API_ATTRIBUTES` — the attribute subset (`name`, `rules_html`, `short_summary`, `bg_color_hex`, `badge_id`) returned by the `suggest` endpoint
- `Tag::ATTRIBUTES_FOR_SERIALIZATION` — the attribute subset used for serializing tag records in the `bulk` response
- `params[:q]` — optional search query for the `index` action; triggers a name search when present
- `params[:tag_ids]` / `params[:tag_names]` — mutually exclusive filters for the `bulk` endpoint; `tag_ids` takes precedence when both are supplied
- `params[:page]` / `params[:per_page]` — pagination parameters for `bulk`; `per_page` is capped at 1000

## Scenarios

### Browsing all tags

1. A visitor requests `GET /tags` without a search query.
2. The controller loads up to 100 direct (non-alias) tags from the current subforem, ordered by hotness score descending.
3. The index view renders each tag as a card showing its name, post count, optional short summary, and follow/hide buttons.
4. The sidebar partial independently queries the top 30 tags by hotness score and displays them as navigation links for unauthenticated visitors; authenticated visitors see their followed tags instead.

### Searching tags by name

1. A visitor submits `GET /tags?q=<query>` via the search form on the index page.
2. The controller performs a name search against the same subforem-scoped tag set.
3. The view heading changes to show "Search results for `<query>`".
4. Only tags whose names match the query are displayed; unrelated tags are excluded.
5. If no tags match, the view displays "No results match that query".

### Fetching tags in bulk by IDs or names

1. A client sends `GET /tags/bulk` with either `tag_ids[]` or `tag_names[]` parameters (or neither for the full paginated list).
2. When `tag_ids` is present, the response includes only tags matching those IDs; when `tag_names` is present instead, it matches by name; when neither is provided, all tags are returned paginated.
3. Results are ordered by `taggings_count` descending and paginated using `page` and `per_page` (default 10, max 1000).
4. The response is a JSON array of tag objects including badge image data.

### Fetching tag suggestions

1. A client sends `GET /tags/suggest`.
2. The controller returns up to 100 tags from the current subforem ordered by hotness score, including a limited attribute set and associated badge image.
3. The response is a JSON array suitable for populating a tag suggestion dropdown or autocomplete widget.

## Failures / Exceptions

- Alias tags (those with a non-empty `alias_for` value) are excluded from the `index` listing because the `tags` helper applies `.direct` scope; they do not appear in search results either.
- The `bulk` endpoint silently ignores `tag_ids` when both `tag_ids` and `tag_names` are provided — `tag_ids` takes precedence because the `if`/`elsif` branch evaluates `tag_ids` first.
