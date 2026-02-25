---
id: "01KJ7GDDAJTJNN577CFGG63JG2"
name: "api_client_can_remove_role_from_user"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/api/v1/user_roles_controller.rb`
- `spec/requests/api/v1/user_roles_spec.rb` (Test)
- `spec/requests/api/v1/docs/user_roles_spec.rb` (Test)

## Functional Overview

An authenticated API client can remove a moderation role from a user by sending a DELETE request to `/api/users/:id/:role`. The allowed roles are `suspend`/`suspended`, `limited`, `spam`, and `trusted`. The system validates the role name, looks up the target user by ID, and checks that the caller has permission to manage user roles via Pundit policy. On success, the target user is reverted to "Good standing" status via `Moderator::ManageActivityAndRoles`, and an audit log entry is written recording the specific role that was removed. The response is 204 No Content.

## Design Intent

Rather than removing a specific role record directly, the destroy action always transitions the user to "Good standing" status. This is intentional: the set of roles handled here (limited, spam, trusted, suspended) represents moderation states that the platform treats as mutually exclusive promotions or restrictions, and "Good standing" is the canonical clean slate. The code comment explicitly notes that removing arbitrary roles would require a different approach.

## Key Members

- `ROLES` — the allowlist of role strings accepted by this endpoint: `suspend`, `suspended`, `limited`, `spam`, `trusted`
- `@user` — the API key owner acting as the admin performing the action
- `@target_user` — the user whose role is being removed, looked up by the `:id` path parameter

## Scenarios

### Successful role removal

1. An API client sends a DELETE request to `/api/users/:id/:role` with a valid API key in the `api-key` header.
2. The system confirms the role name is in the allowed list.
3. The system looks up the target user by ID.
4. Pundit authorizes the caller to manage user roles.
5. The system transitions the target user to "Good standing", effectively removing the moderation role.
6. An audit log entry is created with action `api_user_remove_<role>` and the target user's ID.
7. The system responds with 204 No Content.

### Unauthenticated request

1. A client sends a DELETE request without a valid API key.
2. The system rejects the request and responds with 401 Unauthorized.

### Unauthorized request (non-admin API key)

1. A client sends a DELETE request with an API key belonging to a user who lacks admin or moderator privileges.
2. Pundit denies the `manage_user_roles?` policy check.
3. The system responds with 401 Unauthorized.

### Target user not found

1. A client sends a DELETE request with a valid admin API key but a user ID that does not exist.
2. The system cannot find the user and responds with 404 Not Found.

## Failures / Exceptions

- If the role name is not in the `ROLES` allowlist, a `StandardError` is raised and the system responds with 422 Unprocessable Entity.
- Any other `StandardError` raised during processing (e.g., from the role management service) is caught and returned as 422 Unprocessable Entity with an error message drawn from the target user's validation errors or the exception message.
