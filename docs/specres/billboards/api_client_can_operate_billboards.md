---
id: "01KJ6ENW07FQQ98KJJYN37BF5W"
name: "api_client_can_operate_billboards"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/api/v1/billboards_controller.rb`
- `app/models/billboard.rb`
- `spec/requests/api/v1/billboards_spec.rb` (Test)
- `spec/requests/api/v1/docs/billboards_spec.rb` (Test)

## Functional Overview

The API v1 billboards controller exposes a JSON API for programmatic CRUD management of billboards. Every request must carry a valid API key and the authenticated user must hold the admin role, enforced by `InternalPolicy`. The `index` action returns a paginated list (50 per page, newest first) that can be narrowed with a full-text search term. `show` fetches a single billboard by ID. `create` and `update` persist changes using bang methods that raise on validation failure. A dedicated `unpublish` action sets `published` to `false` without deleting the record. Invalid enum values (e.g., an unrecognized `display_to`) are caught by a `rescue_from ArgumentError` handler and returned as a 422 Unprocessable Entity JSON response.

## Design Intent

Using `save!` / `update!` in create and update lets Rails exceptions propagate to the standard API error handler, keeping the controller thin and avoiding the need to manually check return values and render error forms. The dedicated `unpublish` action uses the non-bang `update` so it can return a 422 with the model's existing error state instead of raising, which allows callers to distinguish a validation failure from a server error. Authentication and authorization are separated into two `before_action` callbacks so that an invalid API key returns 401 while an authenticated non-admin returns 403.

## Key Members

- `permitted_params` — the allowlist of field names accepted in create and update requests; includes `creator_id`, `page_id`, `dismissal_sku`, `weight`, `special_behavior`, `preferred_article_ids`, `prefer_paired_with_billboard_id`, `audience_segment_type`, `exclude_survey_completions`, and `exclude_survey_ids`, in addition to the common content fields. `target_geolocations` is permitted both as a scalar string (comma-separated ISO 3166-2 codes) and as an array.

## Scenarios

### Listing billboards

1. Admin client sends `GET /api/billboards` with a valid API key header.
2. The system returns a JSON array of billboards ordered by descending ID, 50 per page.
3. An optional `search` query parameter narrows results by matching against the billboard name, processed HTML, and placement area.

### Retrieving a single billboard

1. Admin client sends `GET /api/billboards/:id` with a valid API key header.
2. The system looks up the billboard by ID and returns its full JSON representation.
3. If the ID does not exist, the system returns 404.

### Creating a billboard

1. Admin client sends `POST /api/billboards` with a valid API key header and a JSON body containing at least `body_markdown` and `placement_area`.
2. The system validates and saves the new billboard.
3. On success, the system returns the created billboard as JSON with HTTP 201 Created.
4. `target_geolocations` may be supplied as either a comma-separated string (e.g., `"US-WA, CA-BC"`) or a JSON array; both are accepted and stored identically.

### Updating a billboard

1. Admin client sends `PUT /api/billboards/:id` with a valid API key header and a JSON body of fields to change.
2. The system finds the billboard, applies the permitted attributes, and saves.
3. On success, the system returns the updated billboard as JSON with HTTP 200.
4. `target_geolocations` may again be supplied as a string or array.

### Unpublishing a billboard

1. Admin client sends `PUT /api/billboards/:id/unpublish` with a valid API key header.
2. The system sets `published` to `false` on the billboard.
3. On success, the system returns HTTP 204 No Content with no body.
4. If the update fails validation, the system returns the billboard as JSON with HTTP 422.

## Failures / Exceptions

- Missing or invalid API key: controller returns HTTP 401 Unauthorized before any model interaction.
- Authenticated user lacks the admin role: `InternalPolicy` raises a policy error, returning HTTP 403 Forbidden.
- An enum field receives an unrecognized string value (e.g., `display_to: "steve"`): `ArgumentError` is rescued and the system returns HTTP 422 with `{ "error": "...", "status": 422 }`.
- A geolocation code is not a recognized ISO 3166-2 subdivision (e.g., `"US-FAKE"`): model validation fails and the system returns HTTP 422 with an error message identifying the invalid code.
- `create` or `update` encounters other validation errors (e.g., missing `placement_area`): `save!` / `update!` raises `ActiveRecord::RecordInvalid`, which the API error handler converts to HTTP 422.
