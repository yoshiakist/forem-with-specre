---
id: "01KJ7G7F0BZ5ZBSGWV365S2RYC"
name: "api_client_can_assign_role_to_user"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/api/v1/user_roles_controller.rb`
- `spec/requests/api/v1/user_roles_spec.rb` (Test)
- `spec/requests/api/v1/docs/user_roles_spec.rb` (Test)

## Functional Overview

An authenticated API client with admin or moderator privileges can assign a moderation role to a target user by sending a PUT request to `/api/users/:id/:role`. The allowed roles are `suspended` (or `suspend`), `limited`, `spam`, and `trusted`. Before processing the assignment, the system validates the role name, resolves the target user by ID, and checks that the requesting user is authorized to manage user roles via Pundit policy. For the suspend role, the system invokes a dedicated suspension handler that records a required moderator note. For all other roles, a general role-assignment handler is used. In every case, an audit log entry is created and the API returns 204 No Content on success.

## Design Intent

The suspend path is intentionally separated from other roles because suspending a user requires additional data (a moderator note) and triggers a richer set of side effects compared to adding a simple role tag. The use of both `"suspend"` and `"suspended"` as accepted values is preserved for historical compatibility with older API clients.

## Key Members

- `ROLES` — the complete list of assignable role values: `suspend`, `suspended`, `limited`, `spam`, `trusted`
- `SUSPEND_MODE` — the subset (`suspend`, `suspended`) that routes through the suspension handler
- `params[:note]` — moderator-supplied reason, required when suspending a user

## Scenarios

### Assigning the suspended role

1. API client sends `PUT /api/users/:id/suspended` with a valid API key and a `note` parameter.
2. System validates the role name and confirms it is in the allowed list.
3. System looks up the target user by ID.
4. System checks that the requesting user is authorized to manage roles (Pundit `manage_user_roles?`).
5. System suspends the target user and records the provided note.
6. System writes an audit log entry with action `api_user_suspend` and the target user ID.
7. System responds with 204 No Content.

### Assigning a non-suspend role (limited, spam, or trusted)

1. API client sends `PUT /api/users/:id/:role` (where `:role` is `limited`, `spam`, or `trusted`) with a valid API key.
2. System validates the role name and resolves the target user.
3. System checks Pundit authorization for role management.
4. System assigns the titleized role to the target user via the role management handler.
5. System writes an audit log entry with action `api_user_<role>` and the target user ID.
6. System responds with 204 No Content.

### Request without authentication

1. API client sends a PUT request with no API key header.
2. System responds with 401 Unauthorized without processing the role change.

### Request with invalid or insufficient credentials

1. API client sends a PUT request with an invalid API key, or with an API key belonging to a user who lacks admin or moderator privileges.
2. System responds with 401 Unauthorized.

## Failures / Exceptions

- If the `:role` parameter is not one of the allowed values, the system raises a `StandardError` which is caught and returned as 422 Unprocessable Entity with the error message.
- If the target user ID does not exist, the system responds with 404 Not Found.
- If any other error occurs during role assignment (e.g., a model validation failure), the system responds with 422 Unprocessable Entity, using the user model's error message if available, otherwise the exception message.
