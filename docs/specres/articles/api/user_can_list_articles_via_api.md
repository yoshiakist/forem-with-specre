---
id: "01KJCH9K2X9B3K15E69D2AR3ZZ"
name: "user_can_list_articles_via_api"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/concerns/api/articles_controller.rb` — `index` action and `INDEX_ATTRIBUTES_FOR_SERIALIZATION`
- `app/controllers/api/v0/articles_controller.rb` — V0 controller that includes the shared concern
- `app/controllers/api/v1/articles_controller.rb` — V1 controller that includes the shared concern
- `app/services/article_api_index_service.rb` — filtering, sorting, and pagination logic
- `app/views/api/v0/articles/index.json.jbuilder` — V0 index response template
- `app/views/api/v1/articles/index.json.jbuilder` — V1 index response template
- `app/views/api/v0/articles/_article.json.jbuilder` — V0 article partial
- `app/views/api/v1/articles/_article.json.jbuilder` — V1 article partial
- `app/views/api/v0/articles/_flare_tag.json.jbuilder` — V0 flare tag partial
- `app/views/api/v1/articles/_flare_tag.json.jbuilder` — V1 flare tag partial
- `spec/requests/api/v0/articles_spec.rb` (Test)
- `spec/requests/api/v1/articles_spec.rb` (Test)
- `spec/requests/api/v1/docs/articles_spec.rb` (Test)

## Functional Overview

Any client can retrieve a paginated list of published articles via `GET /api/articles` (available in both API v0 and v1). The endpoint delegates filtering and sorting to `ArticleApiIndexService`, which selects the appropriate query strategy based on the query parameters supplied. Without any parameters the response contains featured articles ordered by descending hotness score. Clients can narrow results by a single tag, a comma-separated list of tags, tags to exclude, a username or organisation slug, a predefined state, the number of top days, a collection ID, or a sort direction. Responses are paginated (default 30 per page, configurable up to the server maximum) and the reply sets surrogate-key cache headers that reference every article in the result set.

## Design Intent

The `index` action is deliberately kept thin: all query branching lives in `ArticleApiIndexService` so the controller does not need to know which filter strategy applies. Selecting only `INDEX_ATTRIBUTES_FOR_SERIALIZATION` columns from the database avoids loading heavyweight fields such as `body_markdown` and `processed_html` that are unnecessary for list views. Surrogate-key headers on the response enable efficient edge-cache purging when individual articles change.

## Key Members

- `INDEX_ATTRIBUTES_FOR_SERIALIZATION` — the fixed list of columns loaded from the database for each article in the index response; excludes body and HTML to keep payloads small
- `ArticleApiIndexService#get` — selects among tag, tags (multi), username, state, top, collection, sort, and base query strategies based on which params are present
- `DEFAULT_PER_PAGE` (30) — number of articles returned per page when `per_page` is not specified
- `per_page_max` — upper bound on `per_page`, read from `ApplicationConfig["API_PER_PAGE_MAX"]`, defaulting to 1000

## Scenarios

### Default listing — no params

1. Client sends `GET /api/articles` with no query parameters.
2. The service returns featured, published articles from the current subforem ordered by descending hotness score.
3. The response is paginated at 30 articles per page and includes surrogate-key headers covering the returned article set.

### Filter by single tag

1. Client sends `GET /api/articles?tag=<name>`.
2. If the tag requires approval, only approved articles tagged with that name are returned, ordered by descending publication date.
3. Otherwise, articles tagged with that name are returned ordered by descending hotness score.
4. When `top=N` is also present, results are further restricted to articles published within the last N days and ordered by descending score.

### Filter by multiple tags (inclusion or exclusion)

1. Client sends `GET /api/articles?tags=javascript,css` and/or `tags_exclude=node,java`.
2. Articles matching any of the `tags` values and not matching any of the `tags_exclude` values are returned, ordered by descending score.
3. If both params share a tag, the result set is empty.

### Filter by username or organisation slug

1. Client sends `GET /api/articles?username=<value>`.
2. The service first tries to resolve the value as a user username; if found, that user's published articles are returned ordered by descending publication date.
3. If no matching user exists, the service tries to resolve the value as an organisation slug; if found, the organisation's published articles are returned in the same order.
4. If neither a user nor an organisation is found, an empty array is returned.
5. When `state=all` is also supplied, up to `per_page_max` articles are returned instead of the default 30.

### Filter by state

1. Client sends `GET /api/articles?state=fresh`, `?state=rising`, or `?state=recent`.
2. `fresh` returns articles published in the last 7 hours with fewer than 2 public reactions and a score above −2.
3. `rising` returns articles published in the last 3 days with between 20 and 32 public reactions.
4. `recent` returns all published articles ordered by descending publication date.
5. Any other state value returns an empty array.

### Filter by top N days

1. Client sends `GET /api/articles?top=N`.
2. Published articles from the last N days are returned ordered by descending score.

### Filter by collection

1. Client sends `GET /api/articles?collection_id=<id>`.
2. Published articles belonging to that collection are returned ordered by ascending publication date.

### Sort by publication date descending

1. Client sends `GET /api/articles?sort=desc`.
2. All published articles are returned ordered by descending publication date.
3. Any other sort value returns an empty array.

### Pagination

1. Client specifies `page` and/or `per_page` query parameters.
2. `per_page` is capped at the server's configured maximum.
3. The response contains only the articles for the requested page.

### Cache headers

1. After a successful index response, `Surrogate-Key` headers contain the table-level key `articles` plus the record-level key for every article in the result set.
2. These headers enable targeted cache invalidation at the CDN layer when an article changes.

## Failures / Exceptions

- An unknown `state` value (e.g., `state=all` without a `username`) returns an empty array rather than an error.
- An unknown `sort` value returns an empty array rather than an error.
- A `username` that matches neither a user nor an organisation returns an empty array rather than a 404.
- The `per_page` value is silently capped at `per_page_max`; no error is raised if the client requests more than the maximum.
