---
id: "01KHZ55HBKCF9CFW46K61FMYEQ"
name: "admin_can_create_reaction_via_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/api/v1/reactions_controller.rb`
- `app/services/reaction_handler.rb`
- `app/policies/reaction_policy.rb`
- `spec/requests/api/v1/reactions_spec.rb` (Test)
- `spec/requests/api/v1/docs/reactions_spec.rb` (Test)
- `spec/services/reaction_handler_spec.rb` (Test)
- `spec/policies/reaction_policy_spec.rb` (Test)

## Functional Overview

The `POST /api/reactions` endpoint allows an authenticated admin user to create a reaction (such as a "like") on a reactable resource (Article, Comment, or User). The controller delegates creation to `ReactionHandler.create`, invalidates any cached reaction counts for the target reactable before processing, and returns a JSON payload describing the outcome. If the handler reports success, the response includes the reaction ID, result action, category, reactable ID, and reactable type; the HTTP status is `201 Created` for a new reaction or `200 OK` for an idempotent re-creation. On failure, the endpoint returns a `422 Unprocessable Entity` with an error message.

## Key Members

- `category` — the reaction category (e.g., `"like"`); must be a value from `ReactionCategory.public`
- `reactable_id` — integer ID of the target resource
- `reactable_type` — type of the target resource; one of `Reaction::REACTABLE_TYPES` (e.g., `"Article"`, `"Comment"`, `"User"`)

## Scenarios

### Successful reaction creation

1. An admin user sends a `POST /api/reactions` request with a valid API key and the parameters `category`, `reactable_id`, and `reactable_type`.
2. The controller invalidates the cached reaction counts for the target reactable before delegating to `ReactionHandler.create`.
3. `ReactionHandler.create` succeeds and returns a result with `action: "create"`.
4. The controller responds with HTTP `201 Created` and a JSON body containing `id`, `result`, `category`, `reactable_id`, and `reactable_type`.

### Idempotent re-creation (reaction already exists)

1. An admin user sends a `POST /api/reactions` request for a reactable that already has a reaction from this user.
2. The cache invalidation and `ReactionHandler.create` call proceed as normal.
3. The handler returns success but with an action other than `"create"` (indicating the reaction was found, not newly created).
4. The controller responds with HTTP `200 OK` and the same JSON shape.

### Creation fails due to validation error

1. An admin user sends a `POST /api/reactions` request with invalid or conflicting parameters.
2. Cache keys are invalidated and `ReactionHandler.create` is called.
3. `ReactionHandler.create` returns a failure result with one or more error messages.
4. The controller responds with HTTP `422 Unprocessable Entity` and a JSON body containing `error` and `status: 422`.

### Unauthenticated request is rejected

1. A client sends a `POST /api/reactions` request without an API key.
2. The `authenticate!` before-action halts the request.
3. The controller responds with HTTP `401 Unauthorized`.

### Non-admin authenticated request is rejected

1. A client sends a `POST /api/reactions` request with a valid API key for a non-admin user.
2. Authentication succeeds, but the `require_admin` before-action calls `authorize :reaction, :api?`, which raises an authorization error.
3. The controller responds with HTTP `401 Unauthorized`.

## Failures / Exceptions

- Missing or invalid API key: `401 Unauthorized` returned before any handler logic runs.
- Non-admin user: `401 Unauthorized` returned by the `require_admin` policy check.
- Handler-level validation failure: `422 Unprocessable Entity` with a human-readable error sentence.
