---
id: "01KHYCJNHZ6V29EK1MP1PGSCT6"
name: "api_lists_tags"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/concerns/api/tags_controller.rb
- app/controllers/api/v0/tags_controller.rb
- app/controllers/api/v1/tags_controller.rb
- app/views/api/v0/tags/index.json.jbuilder (Template)
- app/views/api/v1/tags/index.json.jbuilder (Template)
- spec/requests/api/v0/tags_spec.rb (Test)
- spec/requests/api/v1/tags_spec.rb (Test)

## Functional Overview

The API tags endpoint (shared across v0 and v1 via the `Api::TagsController` concern) provides a paginated, public JSON listing of tags scoped to the current subforem. Tags are ordered by popularity (taggings count) and include color and summary metadata. The response sets surrogate keys for edge cache invalidation and cache-control headers for HTTP caching.

## Scenarios

### Client lists tags via API

1. A GET request to `/api/tags` (v0) or `/api/v1/tags` (v1) returns a JSON array of tags.
2. Each tag object includes `id`, `name`, `bg_color_hex`, `text_color_hex`, and `short_summary`.
3. Tags are ordered by `taggings_count` in descending order (most used first).
4. Tags are scoped to the current subforem via `Tag.from_subforem`.

### Client paginates results

1. The endpoint accepts `page` and `per_page` query parameters.
2. Default page size is 10.
3. The maximum page size is capped by the `API_PER_PAGE_MAX` application config setting (default 1000).
4. If the requested `per_page` exceeds the maximum, the maximum is used instead.

### System sets edge cache headers

1. The response includes a `surrogate-key` header containing the global tags table key and individual tag record keys.
2. Cache-control headers are set to enable HTTP-level caching.
