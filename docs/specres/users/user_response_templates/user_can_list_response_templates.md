---
id: "01KJ9KP6TJQ2XAGRZXY6SSR1SZ"
name: "user_can_list_response_templates"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/response_templates_controller.rb`
- `app/models/response_template.rb`
- `app/policies/response_template_policy.rb`
- `spec/requests/response_templates_spec.rb` (Test)

## Functional Overview

The `GET /response_templates` endpoint is a JSON-only API that returns response templates available to the requesting user for use when composing comment replies or handling moderation and admin tasks. When called without a `type_of` parameter, the endpoint returns a hash keyed by template type, with each key mapping to an array of templates in that category. When called with a `type_of` parameter, it returns a flat array containing only templates of that specific type. Authorization is enforced per the requested type: regular users can only list their own `personal_comment` templates, moderators and trusted users can additionally access `mod_comment` and `tag_adjustment` templates, and admins can access `email_reply` and `abuse_report_email_reply` templates. Unauthenticated requests are rejected, and non-JSON requests result in a routing error.

## Design Intent

The endpoint deliberately adapts its authorization policy based on the `type_of` query parameter rather than applying a single flat policy. This design allows the same route to serve multiple contexts (comment reply UI, moderation tooling, admin email workflows) without exposing elevated template categories to lower-privileged callers. The policy scope handles data isolation at the query level, ensuring that a regular user's scope never includes templates they are not entitled to even before authorization checks run.

## Scenarios

### Unauthenticated user is rejected

1. A visitor requests `GET /response_templates` with `Accept: application/json` and no session.
2. The server returns a `401 Unauthorized` response.

### Regular user lists their own personal_comment templates

1. A signed-in user requests `GET /response_templates?type_of=personal_comment` with `Accept: application/json`.
2. The policy scope limits the query to templates owned by that user with `type_of: "personal_comment"`.
3. The endpoint authorizes via `index?`, which permits all authenticated users.
4. The server returns a JSON array containing only the user's own `personal_comment` templates.

### Regular user requests all templates without specifying type_of

1. A signed-in user requests `GET /response_templates` (no `type_of` param) with `Accept: application/json`.
2. The policy scope returns only that user's `personal_comment` templates.
3. The server returns a JSON hash with `"personal_comment"` as the only key, mapping to an array of their templates.

### Regular user is denied access to moderator or admin templates

1. A signed-in regular user requests `GET /response_templates?type_of=mod_comment` or `?type_of=email_reply` with `Accept: application/json`.
2. The endpoint attempts to authorize via `moderator_index?` or `admin_index?` respectively.
3. Pundit raises `NotAuthorizedError` because the user is neither a moderator, trusted user, nor admin.

### Moderator lists mod_comment templates

1. A signed-in tag moderator or trusted user requests `GET /response_templates?type_of=mod_comment` with `Accept: application/json`.
2. The policy scope includes both that user's `personal_comment` templates and all non-personal templates.
3. The endpoint authorizes via `moderator_index?`, which passes for moderators and trusted users.
4. The server returns a JSON array of `mod_comment` templates.

### Moderator requests all templates without specifying type_of

1. A signed-in moderator requests `GET /response_templates` (no `type_of` param) with `Accept: application/json`.
2. The policy scope includes the moderator's personal templates and all mod-level templates.
3. The server returns a JSON hash with keys for each available type (e.g., `"personal_comment"` and `"mod_comment"`), each mapping to an array of templates.

### Admin lists admin-only templates

1. A signed-in admin requests `GET /response_templates?type_of=email_reply` with `Accept: application/json`.
2. The policy scope includes all template types.
3. The endpoint authorizes via `admin_index?`, which passes for admins.
4. The server returns `200 OK` and a JSON array of `email_reply` templates.

## Failures / Exceptions

- Non-JSON request (missing or non-JSON `Accept` header): the `ensure_json_request` before-action raises `ActionController::RoutingError` before the action runs.
- Regular user requesting `mod_comment`, `tag_adjustment`, `email_reply`, or `abuse_report_email_reply` type: Pundit raises `NotAuthorizedError`.
- Moderator requesting `email_reply` or `abuse_report_email_reply` type: Pundit raises `NotAuthorizedError`.
