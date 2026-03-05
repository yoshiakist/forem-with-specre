---
id: "01KJ25K4FS13J2KA8CV6011QN8"
name: "admin_can_update_feedback_message_via_api"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/api/v1/feedback_messages_controller.rb`
- `spec/requests/api/v1/feedback_messages_spec.rb` (Test)

## Functional Overview

Authenticated admin users can update a `FeedbackMessage` record via the `PATCH/PUT /api/v1/feedback_messages/:id` endpoint. The controller enforces two access guards: the request must carry a valid API key (authentication), and the authenticated user must hold the admin role (authorization via Pundit policy). When both guards pass, the controller finds the target record by ID and applies the permitted `status` parameter. On success it responds with the updated record and an HTTP 200 status; if the update fails model validation it responds with HTTP 422. Non-admin or unauthenticated requests are rejected with HTTP 401, and a request for a non-existent record results in HTTP 404.

## Design Intent

Authorization is delegated to Pundit through `authorize :reaction, :api?`, keeping access-control logic outside the controller action itself and making policy rules independently testable. Only the `status` field is whitelisted via strong parameters, limiting the attack surface of the endpoint to the single attribute admins are intended to manage.

## Key Members

- `status` — the only permitted attribute; represents the resolution state of a feedback message (e.g., `"Resolved"`)

## Scenarios

### Unauthenticated request is rejected

1. A client sends a `PATCH /api/v1/feedback_messages/:id` request without an API key.
2. The `authenticate!` before-action halts the request.
3. The API responds with HTTP 401 Unauthorized.

### Authenticated non-admin request is rejected

1. A client sends a valid API key belonging to a non-admin user.
2. Authentication passes, but the `require_admin` before-action calls `authorize :reaction, :api?`, which raises a Pundit authorization error.
3. The API responds with HTTP 401 Unauthorized.

### Record not found

1. An admin client sends a valid request targeting a `FeedbackMessage` ID that does not exist.
2. Authentication and authorization pass.
3. `FeedbackMessage.find` raises `ActiveRecord::RecordNotFound`.
4. The API responds with HTTP 404 Not Found.

### Successful update

1. An admin client sends a `PATCH /api/v1/feedback_messages/:id` request with a body containing `{ "feedback_message": { "status": "<new_status>" } }`.
2. Authentication and authorization pass.
3. The controller finds the `FeedbackMessage` and updates its `status` attribute.
4. The record is persisted successfully.
5. The API responds with the updated `FeedbackMessage` as JSON and HTTP 200 OK.

## Failures / Exceptions

- If the model update fails (e.g., validation error), the API responds with HTTP 422 Unprocessable Entity and returns the feedback message object (which carries validation error details).
