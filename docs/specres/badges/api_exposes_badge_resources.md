---
id: "01KJ6FFA2FH0HVDCGYH9XQB3GG"
name: "api_exposes_badge_resources"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/concerns/api/badges_controller.rb`
- `app/controllers/api/v0/badges_controller.rb`
- `app/controllers/api/v1/badges_controller.rb`
- `app/policies/badge_policy.rb`
- `spec/requests/api/v1/badges_spec.rb` (Test)

## Functional Overview

The API exposes a full set of CRUD operations on Badge resources under `/api/badges`, restricted exclusively to admin users. Both v0 and v1 versions share the same concern-based implementation; v0 authenticates via API key or current session and skips CSRF verification, while v1 uses the standard `authenticate!` filter. Listing is paginated at 50 badges per page in descending creation order. Authorization is enforced before every action via a Pundit policy that grants access only when the requesting user holds any admin role.

## Design Intent

The shared concern (`Api::BadgesController`) lets both API versions stay in sync with a single implementation, reducing duplication. Pundit policy delegation keeps authorization logic outside the controller and centralizes the admin check, making it easy to audit or extend.

## Key Members

- `badge_params` — permits `title`, `description`, `badge_image`, `remote_badge_image_url`, `credits_awarded`, and `allow_multiple_awards`
- Pagination: 50 records per page, ordered by `created_at` descending

## Scenarios

### Listing badges (paginated)

1. An admin authenticates and sends `GET /api/badges`.
2. The API returns up to 50 badges ordered by most-recently created.
3. Additional pages are accessible via the `page` query parameter.

### Fetching a single badge

1. An admin sends `GET /api/badges/:id`.
2. The API finds the badge by ID and returns its JSON representation with HTTP 200.

### Creating a badge

1. An admin sends `POST /api/badges` with valid attributes including title, description, and an image URL.
2. The API creates the badge and responds with HTTP 201 and the new badge's JSON.

### Updating a badge

1. An admin sends `PATCH /api/badges/:id` with one or more permitted attributes.
2. The API updates the record and responds with HTTP 200 and the updated badge's JSON.

### Deleting a badge

1. An admin sends `DELETE /api/badges/:id`.
2. The API destroys the badge and responds with HTTP 204 and no body.

## Failures / Exceptions

- A non-admin user sending any request receives HTTP 401 Unauthorized, enforced by the Pundit `api?` policy check.
- `POST` or `PATCH` with invalid attributes (e.g., blank title) returns HTTP 422 with an `errors` array of full message strings.
