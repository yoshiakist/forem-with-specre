---
id: "01KJ9MXQJ1XD7KP3VER5TAZD8S"
name: "api_client_can_invite_user_via_admin_api"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/concerns/api/admin/users_controller.rb`
- `app/controllers/api/v0/admin/users_controller.rb`
- `app/controllers/api/v1/admin/users_controller.rb`
- `spec/requests/api/v0/admin/users_spec.rb` (Test)
- `spec/requests/api/v1/admin/users_spec.rb` (Test)

## Functional Overview

The admin API exposes a `POST /api/admin/users` endpoint that allows a super-admin API client to invite a new user by email. The shared concern `Api::Admin::UsersController` implements the `create` action, which calls `User.invite!` with the provided email, optional display name, and optional custom invitation email content (subject, message body, and footnote). The invited user is marked as not yet registered. Both the v0 (API-key-or-session authentication) and v1 (Bearer token authentication) controllers include this concern and enforce super-admin authorization before the action executes. On success the endpoint returns HTTP 200 with no body.

## Scenarios

### Successful invitation with email only

1. A super-admin client sends `POST /api/admin/users` with a valid API key and a request body containing `email`.
2. The system derives the username from the email address and calls `User.invite!` with `registered: false`.
3. Devise enqueues an invitation email to the specified address.
4. The endpoint responds with HTTP 200 (no body).
5. A new user record exists in the system with `registered` set to `false`.

### Successful invitation with custom email content

1. A super-admin client sends `POST /api/admin/users` with `email`, `custom_invite_subject`, `custom_invite_message`, and `custom_invite_footnote` in the request body.
2. The system passes these custom fields as options to `User.invite!`, which forwards them to `DeviseMailer.invitation_instructions`.
3. The invitation email is enqueued with the custom subject and message content.
4. The endpoint responds with HTTP 200.

### Rejected request — no authentication token

1. A client sends `POST /api/admin/users` with no API key.
2. The `authenticate_with_api_key_or_current_user!` (v0) or `authenticate!` (v1) before-action halts the request.
3. The endpoint responds with HTTP 401 and no user is created.

### Rejected request — non-super-admin token

1. A client sends `POST /api/admin/users` with an API key belonging to a regular user or a regular admin.
2. Authentication succeeds but the `authorize_super_admin` before-action halts the request.
3. The endpoint responds with HTTP 401 and no user is created.

## Failures / Exceptions

- Requests authenticated as a regular admin (not super-admin) are rejected with HTTP 401, confirming that the endpoint is exclusively super-admin-gated.
- The `email` parameter is required; `params.require(:email)` will raise `ActionController::ParameterMissing` if it is absent, resulting in a 400-level error response.
- The `name` field is optional and is compacted away if blank, so callers may omit it without error.
