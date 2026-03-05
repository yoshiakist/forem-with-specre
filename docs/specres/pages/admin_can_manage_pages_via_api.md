---
id: "01KHZFCNSG1G8YSP3PH4BHXRTW"
name: "admin_can_manage_pages_via_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/api/v1/pages_controller.rb`
- `app/models/page.rb`
- `spec/requests/api/v1/pages_spec.rb` (Test)
- `spec/requests/api/v1/docs/pages_spec.rb` (Test)

## Functional Overview

The `GET /api/pages` and `GET /api/pages/:id` endpoints are publicly accessible and return page records serialized as JSON. The write endpoints — `POST /api/pages`, `PUT /api/pages/:id`, and `DELETE /api/pages/:id` — require both authentication (via API key) and admin authorization (enforced through `InternalPolicy`). A `Page` record requires a title, description, a body in at least one format (markdown, HTML, JSON, or CSS), and a valid template type drawn from `TEMPLATE_OPTIONS`. The slug must be unique across pages within the same subforem and must not conflict with usernames, organization slugs, or podcast slugs. On save, the model converts markdown to HTML, optionally renders content from a linked `PageTemplate`, and busts the cache asynchronously. When a write operation fails validation, the controller returns HTTP 422 and surfaces the error messages in the `X-Error-Text` response header.

## Design Intent

Read endpoints are intentionally left open (no authentication required) so that public-facing page content can be fetched without credentials. Write access is gated behind `InternalPolicy` rather than a simple role check, keeping authorization logic consistent with the rest of the internal API surface.

## Key Members

- `TEMPLATE_OPTIONS` — allowed values: `contained`, `full_within_layout`, `nav_bar_included`, `json`, `css`, `txt`
- `permitted_params` — accepted fields: `title`, `slug`, `description`, `is_top_level_path`, `subforem_id`, `body_json`, `body_markdown`, `body_html`, `body_css`, `remote_social_image_url`, `template`
- `social_image` — a nested `{ url: <string> }` param that is remapped to `remote_social_image_url` before being passed to the model

## Scenarios

### Listing all pages

1. Any client sends `GET /api/pages` without credentials.
2. The controller returns all `Page` records as a JSON array.
3. Each object exposes: `id`, `title`, `slug`, `description`, `is_top_level_path`, `landing_page`, `body_html`, `body_json`, `body_markdown`, `processed_html`, `social_image`, `template`, `subforem_id`, `page_template_id`, `template_data`.

### Retrieving a single page

1. Any client sends `GET /api/pages/:id`.
2. If the page exists, the controller returns it as a JSON object with the same fields as the index response.
3. If no page with that ID exists, the response is HTTP 404.

### Admin creates a page

1. An admin sends `POST /api/pages` with a valid API key and a JSON body containing at least `title`, `description`, a body field, and a `template` value from `TEMPLATE_OPTIONS`.
2. The `require_admin` filter verifies the caller has admin privileges via `InternalPolicy`; unauthenticated or non-admin requests receive HTTP 401.
3. The model validates presence of title and description, confirms the body is not entirely blank, ensures the slug is unique across pages, users, organizations, and podcasts, and converts markdown to HTML if provided.
4. On success the controller returns the created page as JSON with HTTP 200.
5. On validation failure the controller returns HTTP 422 with error details in the `X-Error-Text` response header.

### Admin updates a page

1. An admin sends `PUT /api/pages/:id` with a valid API key and updated fields in the JSON body.
2. Authentication and admin authorization are enforced identically to create.
3. The model re-validates all fields and, if markdown is present, re-renders `processed_html`.
4. On success the updated page is returned as JSON with HTTP 200.
5. On validation failure HTTP 422 is returned with `X-Error-Text` populated.

### Admin deletes a page

1. An admin sends `DELETE /api/pages/:id` with a valid API key.
2. Authentication and admin authorization are enforced identically to create and update.
3. If the record is successfully destroyed, the deleted page is returned as JSON with HTTP 200.
4. If the destroy call fails, HTTP 422 is returned with `X-Error-Text` populated.

## Failures / Exceptions

- Missing or invalid API key on write endpoints → HTTP 401.
- Authenticated but non-admin caller on write endpoints → HTTP 401.
- Validation failure (missing title, blank body, invalid template, duplicate slug) on create or update → HTTP 422 with `X-Error-Text` header containing joined error messages.
- `destroy` returning false (e.g., callbacks prevent deletion) → HTTP 422 with `X-Error-Text` header.
- `GET /api/pages/:id` with an unknown ID → HTTP 404.
