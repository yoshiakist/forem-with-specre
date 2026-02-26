---
id: "01KJCHEJQ8BMDATPDZDH3F5QVX"
name: "user_can_retrieve_article_via_api"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/concerns/api/articles_controller.rb`
- `app/controllers/api/v0/articles_controller.rb`
- `app/controllers/api/v1/articles_controller.rb`
- `app/views/api/v0/articles/show.json.jbuilder` (Template)
- `app/views/api/v1/articles/show.json.jbuilder` (Template)
- `app/views/api/v0/articles/_article.json.jbuilder` (Template)
- `app/views/api/v1/articles/_article.json.jbuilder` (Template)
- `spec/requests/api/v0/articles_spec.rb` (Test)
- `spec/requests/api/v1/articles_spec.rb` (Test)
- `spec/requests/api/v1/docs/articles_spec.rb` (Test)

## Functional Overview

Any client can retrieve a single published article via the public API, either by its numeric ID (`GET /api/articles/:id`) or by its author username and slug (`GET /api/articles/:username/:slug`). Both routes are available on API v0 and v1 without authentication. The response includes the full article payload — including `body_markdown` and `processed_html` — along with metadata fields shared with the index endpoint. Surrogate keys are set on the response to support CDN edge caching. Unpublished articles are never surfaced; requests for them return 404.

## Design Intent

Returning `body_markdown` and `processed_html` only on the single-article show endpoints (not the index) keeps list responses lightweight while still giving API consumers full article content when they drill into a specific item. The surrogate key header enables CDN invalidation on a per-article basis so cached show responses can be purged precisely when an article changes. Scoping the query to `.published.from_subforem` enforces the same visibility rules used everywhere else in the application.

## Key Members

- `SHOW_ATTRIBUTES_FOR_SERIALIZATION` — the column allowlist used in the `SELECT` query; extends `INDEX_ATTRIBUTES_FOR_SERIALIZATION` with `:body_markdown` and `:processed_html`
- `show` — looks up a published article by its numeric `id` parameter and eager-loads the author profile
- `show_by_slug` — looks up a published article by constructing a full path from `/:username/:slug` and delegates rendering to the `show` template
- `set_surrogate_key_header` — attaches the article's surrogate cache key to the response for CDN invalidation
- `set_cache_control_headers` — applied as a `before_action` on both `show` and `show_by_slug` in each versioned controller

## Scenarios

### Retrieve article by ID

1. Client sends `GET /api/articles/:id` with a valid numeric ID of a published article
2. System queries the database for a published, subforem-scoped article matching the ID, selecting only the allowed attributes and eager-loading the author's profile
3. System decorates the record and serializes it into the JSON show template
4. System sets a surrogate key header on the response keyed to the article's cache record key
5. Client receives HTTP 200 with the full article payload, including `body_markdown`, `body_html`, and all index fields

### Retrieve article by username and slug

1. Client sends `GET /api/articles/:username/:slug` with a valid author username and article slug
2. System constructs the canonical path `/:username/:slug` and queries for a published, subforem-scoped article at that path
3. System decorates the record, sets the surrogate key header, and renders the `show` template
4. Client receives HTTP 200 with the same full article payload as the by-ID response

### Article is not published

1. Client requests an article by ID or by slug that exists but is not published
2. System finds no match in the published scope and raises a not-found error
3. Client receives HTTP 404

### Article does not exist

1. Client requests an article with an ID or username/slug combination that does not correspond to any record
2. System finds no matching record and raises a not-found error
3. Client receives HTTP 404

## Failures / Exceptions

- Requesting an unpublished article by ID returns 404 (`Article.published` scope excludes it)
- Requesting an article whose ID does not exist returns 404
- Requesting an article with an unknown username or slug returns 404 (`.find_by!` raises `ActiveRecord::RecordNotFound`)
- No authentication is required; both show routes are publicly accessible and included in the `set_cache_control_headers` before-action
