---
id: "01KHZGVB146XQBKF66V2THG07T"
name: "user_can_retrieve_organization_via_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/concerns/api/organizations_controller.rb`
- `app/controllers/api/v0/organizations_controller.rb`
- `app/controllers/api/v1/organizations_controller.rb`
- `app/views/api/v0/organizations/show.json.jbuilder` (Template)
- `app/views/api/v0/organizations/users.json.jbuilder` (Template)
- `app/views/api/v0/organizations/listings.json.jbuilder` (Template)
- `app/views/api/v1/organizations/show.json.jbuilder` (Template)
- `app/views/api/v1/organizations/users.json.jbuilder` (Template)
- `app/views/api/v1/organizations/listings.json.jbuilder` (Template)
- `app/views/api/v0/shared/_organization.json.jbuilder` (Template)
- `app/views/api/v1/shared/_organization.json.jbuilder` (Template)
- `spec/requests/api/v0/organizations_spec.rb` (Test)
- `spec/requests/api/v1/organizations_spec.rb` (Test)

## Functional Overview

Both v0 and v1 of the public API expose read-only endpoints for retrieving organization data. A caller can look up a single organization by username (v0) or by either numeric ID or slug (v1), receiving a JSON object that includes profile fields, social links, and a `joined_at` timestamp. Both versions also provide sub-resource endpoints to list an organization's members and its published listings, each supporting pagination and respecting the `API_PER_PAGE_MAX` server limit. The v1 API additionally exposes an index endpoint that returns a lightweight summary of all organizations. The shared concern `Api::OrganizationsController` holds the common query and pagination logic for `show`, `users`, `listings`, and `articles`, while `Api::V1::OrganizationsController` overrides `show` to support lookup by both numeric ID and slug.

## Design Intent

The v1 `show` action deliberately preserves the v0 default of username-based lookup while adding ID-based lookup as a secondary strategy. A code comment in the controller acknowledges this departs from strict REST convention but was chosen to avoid breaking existing clients that rely on slug/username routing.

## Key Members

- `SHOW_ATTRIBUTES_FOR_SERIALIZATION` — allowlist of organization fields returned by the `show` endpoint; v1 adds `slug` to the v0 set
- `USERS_FOR_SERIALIZATION` — allowlist of user fields returned by the `users` sub-resource endpoint
- `LISTINGS_FOR_SERIALIZATION` — allowlist of listing fields returned by the `listings` sub-resource endpoint
- `API_PER_PAGE_MAX` — server-side cap on items per page, read from `ApplicationConfig`; defaults to 1000 if unset

## Scenarios

### Retrieve a single organization by username (v0)

1. Client sends `GET /api/organizations/:username`.
2. The controller looks up the organization by username using a `find_by!` that raises `RecordNotFound` if no match exists.
3. The response is a JSON object with `type_of: "organization"` and fields including `id`, `username`, `name`, `summary`, social handles, `url`, `location`, `tech_stack`, `tag_line`, `story`, `joined_at`, and `profile_image`.

### Retrieve a single organization by ID or slug (v1)

1. Client sends `GET /api/organizations/:id_or_slug` with the `application/vnd.forem.api-v1+json` Accept header.
2. The controller first tries to find the organization by numeric ID, then falls back to slug lookup.
3. If neither lookup finds a record, the response is `404 Not Found`.
4. On success, the response is a JSON object with the same fields as the v0 show response plus `slug`.

### List all organizations (v1 index)

1. Client sends `GET /api/organizations` with the v1 Accept header.
2. The controller returns a paginated JSON array where each item contains only the lightweight summary fields: `id`, `name`, `profile_image`, `slug`, `summary`, `tag_line`, and `url`.

### List members of an organization

1. Client sends `GET /api/organizations/:id_or_slug/users` (v0 uses username only; v1 accepts numeric ID or slug).
2. A `before_action` resolves the organization or returns `404 Not Found`.
3. The controller paginates the organization's members, capping results at the lesser of the requested `per_page` and `API_PER_PAGE_MAX`.
4. Each user entry includes profile fields such as `id`, `username`, `name`, social handles, `profile_image`, `website_url`, `location`, `summary`, and `joined_at`. Email is not exposed.

### List published listings of an organization

1. Client sends `GET /api/organizations/:id_or_slug/listings`, optionally filtered by `category`.
2. A `before_action` resolves the organization or returns `404 Not Found`.
3. Only published listings are returned, ordered by `bumped_at` descending and paginated with the same `per_page` / `API_PER_PAGE_MAX` cap.
4. Each listing entry embeds the listing fields, the posting user's details, and a brief organization summary (name, username, slug, profile images).

## Failures / Exceptions

- If the organization cannot be found by the given identifier, all endpoints return `404 Not Found`.
- The v1 `show` action rescues `ArgumentError` (e.g. from a malformed ID) and returns `422 Unprocessable Entity` with an `error` field.
- `per_page` values exceeding `API_PER_PAGE_MAX` are silently clamped to the server maximum.
