---
id: "01KJBWZNKHZTQ5XK6XHC5EC3VE"
name: "moderator_can_unpublish_all_user_articles"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/moderator/unpublish_all_articles.rb`
- `app/workers/moderator/unpublish_all_articles_worker.rb`
- `app/views/admin/users/modals/_unpublish_modal.html.erb` (Template)
- `app/views/admin/users/show/unpublish_logs/_index.html.erb` (Template)
- `spec/services/moderator/unpublish_all_articles_spec.rb` (Test)
- `spec/workers/moderator/unpublish_all_articles_worker_spec.rb` (Test)

## Functional Overview

When a moderator or admin initiates a bulk unpublish action against a target user, the system unpublishes all of the user's published articles and soft-deletes all of their non-deleted comments. For articles that contain YAML frontmatter, the `published: true` field is rewritten to `published: false` in the body markdown. After each article is unpublished, related "Published" notifications and context notifications are removed. The entire operation is recorded as an audit log entry, with the action slug reflecting whether the caller is a moderator (`unpublish_all_articles`) or an API actor (`api_user_unpublish`). The work is dispatched asynchronously via a Sidekiq worker on the medium-priority queue.

## Design Intent

Comments are soft-deleted (the `deleted` boolean is set to `true` rather than the records being destroyed) to allow the operation to be reverted. The listener parameter lets the same service record different audit log categories depending on the calling context (admin UI vs. API), keeping audit trails accurate without duplicating business logic.

## Key Members

- `target_user_id` — the user whose articles and comments are being unpublished
- `action_user_id` — the moderator or admin performing the action
- `listener` — audit context; `:moderator` for admin UI actions, `:admin_api` for API-triggered actions (default)
- `ALLOWED_LISTENERS` — whitelist of valid listener values in the worker; invalid values fall back to `:admin_api`

## Scenarios

### Moderator unpublishes all articles for a user

1. A moderator submits the unpublish confirmation form for a target user from the admin panel.
2. The system enqueues `Moderator::UnpublishAllArticlesWorker` with the target user ID, the acting user ID, and the `moderator` listener.
3. The worker validates the listener value and calls `Moderator::UnpublishAllArticles`.
4. The service marks all of the user's published articles as unpublished and, for articles with frontmatter, updates the `published` field in the body markdown to `false`.
5. For each unpublished article, "Published" notifications and context notifications are removed.
6. All of the user's non-deleted comments are soft-deleted by setting `deleted: true`.
7. An audit log entry is created under the moderator category with the slug `unpublish_all_articles`, recording the IDs of affected articles and comments.

### Admin API unpublishes all articles for a user

1. An API request triggers the unpublish action for a target user with the default `admin_api` listener.
2. The worker enqueues and calls `Moderator::UnpublishAllArticles` with `listener: :admin_api`.
3. The service performs the same article and comment unpublishing steps.
4. An audit log entry is created under the admin API category with the slug `api_user_unpublish`.

### Worker receives an invalid listener value

1. The worker is enqueued with a listener string that is not in `ALLOWED_LISTENERS`.
2. The worker falls back to the default listener `:admin_api` before calling the service.
3. The service proceeds normally and the audit log is recorded under the admin API category.

### Target user does not exist

1. The service is called with a `target_user_id` that does not correspond to any user record.
2. The service exits early without performing any unpublishing or audit logging.

## Failures / Exceptions

- If the target user is not found, the service returns without raising an error or modifying any data.
- Invalid listener values passed to the worker are silently replaced with the default `:admin_api` listener.
- Article saves are performed without validation (`save(validate: false)`) to avoid blocking the operation on validation errors.
