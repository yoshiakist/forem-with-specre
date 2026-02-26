---
id: "01KJCHTC22WA5N8C2J29GQ6Q76"
name: "user_can_list_own_articles_via_api"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/concerns/api/articles_controller.rb` (Implementation — `me` action and `ME_ATTRIBUTES_FOR_SERIALIZATION`)
- `app/controllers/api/v0/articles_controller.rb` (Controller — V0, requires `authenticate!` for `me`)
- `app/controllers/api/v1/articles_controller.rb` (Controller — V1, requires `authenticate_with_api_key!` for `me`)
- `app/views/api/v0/articles/me.json.jbuilder` (View — V0 response template)
- `app/views/api/v1/articles/me.json.jbuilder` (View — V1 response template)
- `app/views/api/v0/articles/_article.json.jbuilder` (Partial — V0 article shape)
- `app/views/api/v1/articles/_article.json.jbuilder` (Partial — V1 article shape)
- `spec/requests/api/v0/articles_spec.rb` (Test)
- `spec/requests/api/v1/articles_spec.rb` (Test)
- `spec/requests/api/v1/docs/articles_spec.rb` (Test — OpenAPI contract tests)

## Functional Overview

An authenticated user can retrieve a paginated list of their own articles by calling `GET /api/articles/me` (optionally suffixed with `/published`, `/unpublished`, or `/all`). The endpoint requires a valid API key and returns only articles belonging to the requesting user, including the `body_markdown` field which is absent from the public article index. By default, only published articles are returned in reverse chronological publication order. An explicit `status` parameter controls whether published, unpublished, or all articles are returned. Pagination is supported via `page` and `per_page` parameters (default 30, capped by the server-configured maximum).

## Design Intent

The `/me` endpoint provides a private, authenticated view of a user's own content distinct from the public article listing. Including `body_markdown` allows clients (editors, importers, publishing tools) to round-trip full article content. Filtering by publication status lets authors manage their drafts without a separate drafts API. Ordering unpublished articles by creation time (most recent first) prioritizes recently created drafts at the top when mixing statuses.

## Key Members

- `ME_ATTRIBUTES_FOR_SERIALIZATION` — the fixed attribute list selected from the database for this endpoint: `id`, `user_id`, `organization_id`, `title`, `description`, `main_image`, `published`, `published_at`, `cached_tag_list`, `slug`, `path`, `canonical_url`, `comments_count`, `public_reactions_count`, `page_views_count`, `crossposted_at`, `body_markdown`, `updated_at`, `reading_time`
- `params[:status]` — optional filter; accepted values: `"published"`, `"unpublished"`, `"all"`; defaults to published when omitted or unrecognized
- `params[:page]` — page number for cursor-based pagination
- `params[:per_page]` — number of articles per page; capped at `API_PER_PAGE_MAX` (default 1000)

## Scenarios

### Default request returns only the authenticated user's published articles

1. Authenticated user sends `GET /api/articles/me` with a valid API key.
2. The system scopes the query to that user's published articles only.
3. Articles are ordered by `published_at` descending, then `created_at` descending.
4. The first page (up to 30 articles) is returned as JSON, each article including `body_markdown`.

### Requesting published articles explicitly

1. Authenticated user sends `GET /api/articles/me/published`.
2. The system applies the `published` scope, equivalent to the default behavior.
3. Only published articles belonging to the user are returned.

### Requesting unpublished (draft) articles

1. Authenticated user sends `GET /api/articles/me/unpublished`.
2. The system applies the `unpublished` scope.
3. Only unpublished articles belonging to the user are returned, ordered by `created_at` descending.

### Requesting all articles regardless of publication status

1. Authenticated user sends `GET /api/articles/me/all`.
2. The system applies no publication filter, returning both published and unpublished articles.
3. Unpublished articles appear at the top (no `published_at`), followed by published articles in reverse chronological order.

### Paginating results

1. Authenticated user sends `GET /api/articles/me` with `page=2&per_page=2`.
2. The system returns the second page of two articles.
3. If fewer than `per_page` articles remain, only those remaining are returned.

### Unauthenticated request is rejected

1. A client sends `GET /api/articles/me` without a valid API key.
2. The system responds with HTTP 401 Unauthorized and no article data.

## Failures / Exceptions

- Missing or invalid API key: HTTP 401 Unauthorized is returned immediately; the `me` action is never reached.
- `per_page` exceeding the server maximum (`API_PER_PAGE_MAX`): capped silently to the configured maximum.
- An unrecognized `status` value (anything other than `"published"`, `"unpublished"`, `"all"`): treated as the default and returns only published articles.
