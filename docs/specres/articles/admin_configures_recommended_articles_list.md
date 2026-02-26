---
id: "01KJBV555EB91576QYQPCRJSP1"
name: "admin_configures_recommended_articles_list"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/models/recommended_articles_list.rb`
- `app/controllers/api/v1/recommended_articles_lists_controller.rb`
- `spec/models/recommended_articles_list_spec.rb` (Test)
- `spec/requests/api/v1/recommended_articles_lists_spec.rb` (Test)
- `spec/factories/recommended_articles_lists.rb` (Test)

## Functional Overview

Administrators can manage named lists of recommended articles through a dedicated admin-only API. Each list belongs to a user, targets a placement area (currently only `main_feed`), carries an ordered set of article IDs, and automatically expires after one day unless an explicit expiry is provided. The create endpoint behaves as an upsert: if a list already exists for the same user and placement area it is updated in place rather than duplicated. The API enforces authentication via API key and authorization via admin role on every action.

## Key Members

- `name` — human-readable label for the list; required, maximum 120 characters
- `placement_area` — enum that determines where the list is rendered; only `main_feed` is currently supported
- `article_ids` — ordered array of integer article IDs; accepts either a comma-separated string or a native array, with blank and nil entries filtered out
- `expires_at` — timestamp after which the list is considered inactive; defaults to one day from creation if omitted

## Scenarios

### Admin lists all recommended articles lists

1. Admin sends a GET request to `GET /api/v1/recommended_articles_lists` with a valid API key.
2. The system verifies the key and confirms the caller has the admin role.
3. The system returns a paginated JSON array of all lists ordered by descending ID, up to 50 per page.
4. If a `search` parameter is present, results are filtered to matching lists before pagination.

### Admin retrieves a single recommended articles list

1. Admin sends a GET request to `GET /api/v1/recommended_articles_lists/:id` with a valid API key.
2. The system locates the list by ID and returns it as JSON.

### Admin creates (or upserts) a recommended articles list

1. Admin sends a POST request to `POST /api/v1/recommended_articles_lists` with a valid API key and a payload containing `name`, `placement_area`, `user_id`, `article_ids`, and optionally `expires_at`.
2. The system looks up an existing list for the given `user_id` and `placement_area`; if found it updates it, otherwise it initializes a new record.
3. The record is saved; if `expires_at` was omitted, it is set to one day from now before saving.
4. The system responds with the saved list as JSON and HTTP 201 Created.

### Admin updates an existing recommended articles list

1. Admin sends a PUT request to `PUT /api/v1/recommended_articles_lists/:id` with a valid API key and updated attributes.
2. The system locates the list by ID, applies the permitted attributes, and saves.
3. The system responds with the updated list as JSON and HTTP 200.

### Unauthenticated or unauthorized request is rejected

1. A caller sends any request without a valid API key, or with a key whose user lacks the admin role.
2. The system returns HTTP 401 Unauthorized and does not expose any list data.

## Failures / Exceptions

- An `ArgumentError` raised during parameter processing is rescued and returns a 422 Unprocessable Entity response.
- Saving with invalid attributes (e.g., blank name or name exceeding 120 characters) raises an `ActiveRecord::RecordInvalid` exception propagated to the standard API error handler.
