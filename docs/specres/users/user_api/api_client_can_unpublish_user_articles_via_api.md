---
id: "01KJ9N6FHMP17NN9KTJQQEMB8P"
name: "api_client_can_unpublish_user_articles_via_api"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/concerns/api/users_controller.rb`
- `spec/requests/api/v1/users_spec.rb` (Test)

## Functional Overview

An authenticated API client with admin privileges can trigger a bulk unpublish of all articles and comments belonging to a target user by sending `PUT /api/users/:id/unpublish`. The system authorizes the request via the `unpublish_all_articles?` policy, enqueues `Moderator::UnpublishAllArticlesWorker` to perform the actual unpublishing asynchronously, and records a `Note` on the target user documenting who initiated the action and why. The endpoint responds immediately with 204 No Content without waiting for the worker to complete.

## Design Intent

The unpublish action is intentionally asynchronous: bulk content removal can involve many records and must not block the HTTP response. The Note record provides a persistent, human-readable audit trail separate from the structured `AuditLog`, allowing moderators to capture free-form context alongside the machine-readable log of affected content IDs.

## Key Members

- `PUT /api/users/:id/unpublish` — the API endpoint; `:id` is the numeric ID of the target user
- `unpublish_all_articles?` — Pundit policy method that restricts this action to authorized admins
- `Moderator::UnpublishAllArticlesWorker` — background worker that unpublishes articles and soft-deletes comments for the target user
- `Note` — model record created on the target user with `reason: "unpublish_all_articles"` to document the moderation action
- `params[:note]` — optional free-text note; falls back to a default message when absent

## Scenarios

### Successful unpublish with default note

1. An authenticated admin API client sends `PUT /api/users/:id/unpublish` with no `note` parameter
2. The system authorizes the request using the `unpublish_all_articles?` policy
3. The system enqueues `Moderator::UnpublishAllArticlesWorker` with the target user's ID and the requesting user's ID
4. The system creates a `Note` on the target user with `reason: "unpublish_all_articles"` and content set to `"<requester_username> requested unpublish all articles via API"`
5. The system responds with 204 No Content
6. The worker asynchronously unpublishes all of the target user's published articles and soft-deletes their comments

### Successful unpublish with custom note

1. An authenticated admin API client sends `PUT /api/users/:id/unpublish` with a non-empty `note` parameter
2. The system authorizes the request using the `unpublish_all_articles?` policy
3. The system enqueues `Moderator::UnpublishAllArticlesWorker` for the target user
4. The system creates a `Note` on the target user with `reason: "unpublish_all_articles"` and content set to the value of `params[:note]`
5. The system responds with 204 No Content

### Unauthorized — unauthenticated or non-admin caller

1. A client sends `PUT /api/users/:id/unpublish` with no API key, an invalid API key, or an API key belonging to a non-admin user
2. The system rejects the request and responds with 401 Unauthorized
3. No worker is enqueued and no Note is created

## Failures / Exceptions

- If the target user ID does not correspond to an existing user, the system raises a not-found error (standard Rails `ActiveRecord::RecordNotFound` handling)
- If the caller lacks the `unpublish_all_articles?` privilege, Pundit raises an authorization error and the request is rejected before any side effects occur
