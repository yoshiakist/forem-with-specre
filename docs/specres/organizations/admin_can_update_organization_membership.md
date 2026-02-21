---
id: "01KJ02QR77TXF2XJR4QS32QAAE"
name: "admin_can_update_organization_membership"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/organization_memberships_controller.rb`
- `app/models/organization_membership.rb`
- `spec/requests/admin/organization_memberships_spec.rb` (Test)
- `app/views/admin/users/modals/_add_organization_modal.html.erb` (Template)

## Functional Overview

Super-admin users can manage which organizations a user belongs to through three operations: adding a user to an organization with a given role, changing an existing membership's role, and removing a user from an organization entirely. All three operations are available both as standard HTML form submissions (which redirect with flash messages) and as Ajax/JSON requests (which return a JSON payload with a `result` or `error` key). The `OrganizationMembership` model enforces that `type_of_user` must be one of `admin`, `member`, `guest`, or `pending`, and that a user can only hold one membership per organization. After every change the organization's cache is busted and the user's `organization_info_updated_at` timestamp is touched.

## Scenarios

### Admin adds a user to an organization (HTML)

1. An authenticated super-admin submits a form with `user_id`, `organization_id`, and a valid `type_of_user` (e.g., `member` or `admin`).
2. The system looks up the organization by `organization_id`.
3. If the organization exists and the membership record saves successfully, the system sets a success flash message and redirects to the user's admin detail page (or the admin users list if the referer does not match the user detail path).
4. The new `OrganizationMembership` record is persisted, `organization_info_updated_at` on the user is updated, and the organization's cache is busted.

### Admin adds a user to an organization (Ajax/JSON)

1. An authenticated super-admin sends an XHR POST with `user_id`, `organization_id`, and a valid `type_of_user`.
2. The system looks up the organization and attempts to save the membership.
3. On success it returns HTTP 201 Created with `{ "result": "<success message>" }`.
4. If the organization does not exist it returns HTTP 422 Unprocessable Entity with `{ "error": "<not-found message>" }`.
5. If the membership record is invalid (e.g., `type_of_user` not in the allowed list, or the user is already a member of that organization) it returns HTTP 422 Unprocessable Entity with `{ "error": "<validation errors>" }`.

### Admin changes a membership role (HTML)

1. An authenticated super-admin submits a form targeting an existing membership, providing a new `type_of_user` value.
2. Only `type_of_user` is permitted for update; `user_id` and `organization_id` are ignored even if supplied, preserving the existing membership's user and organization.
3. If the update succeeds, the system sets a success flash message and redirects to the user's admin detail page.
4. If the value is invalid (not in `USER_TYPES`), the system sets a danger flash message with the validation error and redirects to the same page without changing the record.

### Admin changes a membership role (Ajax/JSON)

1. An authenticated super-admin sends an XHR PUT with the membership ID and a new `type_of_user`.
2. On success it returns HTTP 200 OK with `{ "result": "<success message>" }`.
3. On validation failure it returns HTTP 422 Unprocessable Entity with `{ "error": "<validation errors>" }`.
4. If the membership ID does not exist the system raises `ActiveRecord::RecordNotFound`, resulting in a 404 response.

### Admin removes a user from an organization (HTML and Ajax/JSON)

1. An authenticated super-admin sends a DELETE request targeting an existing membership record.
2. The system destroys the membership record.
3. On success via HTML, a success flash message is set and the browser is redirected to the user's admin detail page.
4. On success via Ajax, HTTP 200 OK is returned with `{ "result": "<success message>" }`.
5. After destruction, the user's `organization_info_updated_at` is updated and the organization's cache is busted.
6. If destruction fails via Ajax, HTTP 500 Internal Server Error is returned with `{ "error": "<failure message>" }`.
7. If the membership ID does not exist the system raises `ActiveRecord::RecordNotFound`, resulting in a 404 response.

## Failures / Exceptions

- If `organization_id` is not provided or refers to a non-existent organization during create, the membership is not saved and the admin sees an error stating the organization does not exist.
- If `type_of_user` is not one of `admin`, `member`, `guest`, or `pending`, the `OrganizationMembership` model's inclusion validation fails and the error message "not included in the list" is surfaced to the admin.
- If a user is already a member of the given organization, the uniqueness validation on `user_id` scoped to `organization_id` prevents a duplicate membership from being created.
- Attempts to change `user_id` or `organization_id` during an update are silently ignored because those parameters are not permitted by the update strong-parameters filter.
- On destroy, if `OrganizationMembership#destroy` returns false (e.g., due to a callback halt), the JSON endpoint returns HTTP 500 with an error message; the HTML endpoint sets a danger flash.
