---
id: "01KJ41E1Q931QJ3XZVWRJJ1PJX"
name: "user_can_list_tags_via_api"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/concerns/api/tags_controller.rb`
- `app/controllers/api/v0/tags_controller.rb`
- `app/controllers/api/v1/tags_controller.rb`
- `spec/requests/api/v0/tags_spec.rb` (Test)
- `spec/requests/api/v1/tags_spec.rb` (Test)
- `spec/requests/api/v1/docs/tags_spec.rb` (Test)

## Functional Overview

The `GET /api/tags` endpoint allows clients to retrieve a paginated list of tags available for use on articles. The shared logic lives in `Api::TagsController` concern and is included by both the v0 and v1 versioned controllers, which each apply response caching headers before the action runs. Tags are selected with a fixed set of serialization attributes (`id`, `name`, `bg_color_hex`, `text_color_hex`, `short_summary`), scoped to the current subforem, and returned ordered by popularity (taggings count, descending). Pagination is controlled by `page` and `per_page` query parameters, with `per_page` defaulting to 10 and capped by the `API_PER_PAGE_MAX` application configuration value (defaulting to 1000). Surrogate cache keys covering the tag table and each returned tag record are set on the response to support edge caching.

## Design Intent

The behavior is extracted into a shared concern so that both API versions expose identical tag listing logic without duplication. The hard cap on `per_page` from `API_PER_PAGE_MAX` allows operators to limit response size at the infrastructure level without code changes.

## Key Members

- `page` — query parameter selecting the page number for pagination
- `per_page` — query parameter controlling results per page; defaults to 10, capped at `API_PER_PAGE_MAX`
- `ATTRIBUTES_FOR_SERIALIZATION` — frozen list of tag fields included in the response: `id`, `name`, `bg_color_hex`, `text_color_hex`, `short_summary`

## Scenarios

### Successful tag listing

1. Client sends a `GET` request to `/api/tags` (v0 or v1).
2. The controller applies cache control headers before processing.
3. The system queries tags scoped to the current subforem, selecting only the serialization attributes, ordered by taggings count descending.
4. The response contains the list of tags as JSON with fields `id`, `name`, `bg_color_hex`, `text_color_hex`, and `short_summary`.

### Paginated listing

1. Client sends a `GET` request to `/api/tags` with `page` and `per_page` query parameters.
2. The system returns only the tags for the requested page, up to `per_page` results.
3. Subsequent requests with an incremented `page` value return the next slice of results.

### Per-page cap enforcement

1. Client requests more results per page than the configured `API_PER_PAGE_MAX`.
2. The system silently reduces the effective page size to `API_PER_PAGE_MAX`, returning no more than that many results regardless of the requested value.

### Edge cache key assignment

1. After building the response, the system sets surrogate cache keys on the response headers, including the tags table key and the record key for each returned tag.
2. This allows downstream edge caches to invalidate cached responses when tag data changes.
