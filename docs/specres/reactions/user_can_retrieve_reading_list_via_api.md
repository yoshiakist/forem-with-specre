---
id: "01KJXS159QDWN1VEG2HY67NM54"
name: "user_can_retrieve_reading_list_via_api"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/controllers/concerns/api/readinglist_controller.rb`
- `app/controllers/api/v0/readinglist_controller.rb`
- `app/controllers/api/v1/readinglist_controller.rb`
- `spec/requests/api/v0/readinglist_spec.rb` (Test)
- `spec/requests/api/v1/readinglist_spec.rb` (Test)

## Functional Overview

An authenticated user can retrieve their reading list via `GET /api/readinglist`. The shared concern queries the user's non-archived `readinglist` reactions, paginated with a default of 30 per page and a maximum of 100. For each reaction, the associated article (with its organization and author data) is fetched and assembled into a response. V0 authenticates via session, while V1 requires an API key with the `application/vnd.forem.api-v1+json` Accept header.

## Design Intent

The core `index` logic lives in a shared concern (`Api::ReadinglistController`) that both the V0 and V1 versioned controllers include. This avoids duplication while allowing each API version to enforce its own authentication strategy: V0 uses `authenticate!` (session-based), while V1 uses `authenticate_with_api_key!`.

## Key Members

- `PER_PAGE_MAX` — upper bound (100) on items returned per page, regardless of the `per_page` query parameter
- `INDEX_REACTIONS_ATTRIBUTES_FOR_SERIALIZATION` — the minimal set of reaction columns selected (`id`, `reactable_id`, `created_at`, `status`) to keep the query lean
- `params[:page]` / `params[:per_page]` — pagination controls; `per_page` defaults to 30

## Scenarios

### Unauthenticated request is rejected

1. A client sends `GET /api/readinglist` without a valid API key or session.
2. The API returns `401 Unauthorized`.

### Authenticated user retrieves their reading list

1. An authenticated user sends `GET /api/readinglist` with a valid API key.
2. The API queries the user's non-archived `readinglist` reactions ordered by newest first.
3. For each reaction, the associated article (with author and organization) is fetched.
4. The response body is JSON with HTTP `200 OK`.

### Archived reactions are excluded

1. A user has both active and archived reading reactions.
2. The user sends `GET /api/readinglist`.
3. Only the non-archived reactions are returned; archived ones are omitted.

### Reading list is paginated

1. A user has more reading reactions than the requested page size.
2. The user sends `GET /api/readinglist` with `page` and `per_page` query parameters.
3. The API returns at most `per_page` items (capped at 100) for the requested page.

### Reading list is scoped to the requesting user

1. Multiple users have reading reactions.
2. An authenticated user requests `GET /api/readinglist`.
3. The response contains only reactions belonging to that user, not reactions from other users.

## Failures / Exceptions

- If the API key is invalid or missing, the endpoint returns `401 Unauthorized`.
