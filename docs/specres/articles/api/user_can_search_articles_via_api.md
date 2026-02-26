---
id: "01KJCHXPSF9DJHF0B8M4XZRZZD"
name: "user_can_search_articles_via_api"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/concerns/api/articles_controller.rb`
- `app/controllers/api/v0/articles_controller.rb`
- `app/controllers/api/v1/articles_controller.rb`
- `app/queries/articles/api_search_query.rb`
- `app/views/api/v0/articles/search.json.jbuilder`
- `app/views/api/v1/articles/search.json.jbuilder`
- `app/views/api/v0/articles/_article.json.jbuilder`
- `app/views/api/v1/articles/_article.json.jbuilder`
- `app/views/api/v0/articles/_flare_tag.json.jbuilder`
- `app/views/api/v1/articles/_flare_tag.json.jbuilder`
- `spec/requests/api/v0/articles_spec.rb` (Test)
- `spec/requests/api/v1/articles_spec.rb` (Test)
- `spec/queries/articles/api_search_query_spec.rb` (Test)

## Functional Overview

Any client can issue a `GET /api/articles/search` request (no authentication required) to search published articles by keyword or to retrieve the most popular articles within a recent time window. The endpoint delegates query execution to `Articles::ApiSearchQuery`, which filters to published, subforem-scoped articles meeting the minimum score threshold, then optionally applies full-text search via the `q` parameter or a time-window popularity filter via the `top` parameter. Results are paginated (default 30 per page, capped by `API_PER_PAGE_MAX`). The response shape adapts to result count: when exactly one article is returned, the full `body_markdown` is included; when more than one article is returned, `body_markdown` is omitted to keep the response size manageable for external consumers such as the ChatGPT plugin.

## Design Intent

This endpoint was introduced as an intentional addition alongside the existing `GET /api/articles` index endpoint, specifically to support the ChatGPT plugin without modifying the established index contract. Separating the search endpoint allows independent experimentation—including the `body_markdown` toggle—without risk of breaking existing API consumers. The `top` filter is expressed as a number of days, giving callers a simple way to retrieve trending content without building date arithmetic themselves.

## Key Members

- `q` — free-text search string; when present, articles are filtered to those whose content matches the query via `Article#search_articles`
- `top` — integer number of days; when present, restricts results to articles published within the last N days and sorts by descending `score`
- `page` / `per_page` — pagination controls; `per_page` is capped at `API_PER_PAGE_MAX` (defaults to 1000 if unset in config), and defaults to 30
- `INDEX_ATTRIBUTES_FOR_SERIALIZATION` — column list used for multi-result responses (excludes `body_markdown`)
- `ADDITIONAL_SEARCH_ATTRIBUTES_FOR_SERIALIZATION` — column list used for single-result responses (adds `body_markdown` to the index list)
- Baseline filter: only published articles from the current subforem with `score >= Settings::UserExperience.index_minimum_score`, ordered by `hotness_score` descending

## Scenarios

### Search by keyword

1. Client sends `GET /api/articles/search?q=ruby`
2. The system filters published, score-qualified articles whose content matches "ruby" and returns them ordered by hotness score
3. If more than one article matches, the response is a JSON array of article objects without `body_markdown`
4. If exactly one article matches, the response includes `body_markdown` in addition to all standard index fields

### Filter by top articles within a time window

1. Client sends `GET /api/articles/search?top=7`
2. The system restricts results to articles published within the last 7 days and sorts them by descending score
3. The response is a JSON array of article objects; `body_markdown` is included only if the result set contains exactly one article

### Search with no parameters

1. Client sends `GET /api/articles/search` with no query parameters
2. The system returns all published, score-qualified articles in the current subforem, ordered by hotness score
3. Response structure follows the same single-vs-multiple article rule for `body_markdown`

### Pagination

1. Client supplies `page` and `per_page` parameters
2. The system returns the requested page slice; `per_page` is silently capped at `API_PER_PAGE_MAX` if the requested value exceeds it

### CORS support

1. Client sends the request with an `Origin` header
2. The server responds with appropriate `Access-Control-Allow-*` headers, permitting cross-origin reads

## Failures / Exceptions

- Articles that are unpublished or belong to a different subforem are never included in results, regardless of parameters
- Articles whose `score` falls below `Settings::UserExperience.index_minimum_score` are excluded even when the `q` parameter matches their content
- When both `q` and `top` are supplied, `top` takes precedence: results are filtered to the time window and sorted by score, but the `q` full-text filter is also applied first before the `top` filter narrows results further
- Missing `social_image` or `main_image` values do not cause errors; the fields are returned as `null`
