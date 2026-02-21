---
id: "01KJ1623YBY62EQ349V4X1XPFP"
name: "system_updates_notifications_on_content_change"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/update.rb`
- `app/workers/notifications/update_worker.rb`
- `spec/services/notifications/update_spec.rb` (Test)
- `spec/workers/notifications/update_worker_spec.rb` (Test)

## Functional Overview

When an article or comment is modified, the system refreshes the cached JSON payload stored in all matching `Notification` records so that notification recipients always see current content. `Notifications::Update` is the synchronous service that performs this refresh; `Notifications::UpdateWorker` is the Sidekiq job that resolves the notifiable object from its database ID and class name before delegating to the service. Only `Article` and `Comment` are supported notifiable types; attempts to update notifications for any other type are either silently skipped (service) or raise `InvalidNotifiableForUpdate` (worker).

## Design Intent

The worker validates the notifiable class before hitting the database, failing fast with a named error rather than letting an unexpected constant be materialized via `constantize`. The service uses `update_all` (a single SQL statement) rather than loading individual records to avoid unnecessary memory allocation, and uses `.none?` instead of `.blank?` for the same reason — it avoids loading all matched rows just to check emptiness.

## Key Members

- `notifiable` — the `Article` or `Comment` whose change triggered the update
- `action` — optional scoping string (e.g., `"Published"`) used to match only notifications recorded for that specific action
- `json_data` — the denormalized JSON blob stored on each `Notification` record, rebuilt from helper methods delegated to the `Notifications` module

## Scenarios

### Article notifications refreshed without organization

1. An article is saved and a background job enqueues `Notifications::UpdateWorker` with the article's ID, the string `"Article"`, and an optional action.
2. The worker looks up the article by ID; if not found it returns without calling the service.
3. The service finds all `Notification` records whose `notifiable_id`, `notifiable_type`, and `action` match the article.
4. If no matching notifications exist, the service returns without performing any write.
5. The service rebuilds the JSON payload with article data and author user data (no organization key), then bulk-updates all matching notifications in a single statement.

### Article notifications refreshed with organization

1. An article belonging to an organization is saved and the update worker is triggered.
2. The service finds matching notifications and detects that the notifiable is an `Article` with an associated organization.
3. The rebuilt JSON payload includes article data, author user data, and organization data.
4. All matching notifications are bulk-updated with the enriched payload.

### Comment notifications refreshed

1. A comment is saved and `Notifications::UpdateWorker` is enqueued with the comment's ID and `"Comment"`.
2. The service finds all `Notification` records for that comment (action defaults to `nil`).
3. The rebuilt payload contains comment data and the commenter's user data (no organization key).
4. All matching notifications are bulk-updated.

### Unsupported notifiable type rejected by worker

1. The worker receives a notifiable class name that is not `"Article"` or `"Comment"` (e.g., `"User"`).
2. The worker raises `Notifications::InvalidNotifiableForUpdate` immediately, before any database lookup.

### Unsupported notifiable type silently skipped by service

1. The service is called directly with an object that is neither an `Article` nor a `Comment` (e.g., a `Reaction`).
2. The service returns without querying or modifying any notifications.

## Failures / Exceptions

- `Notifications::InvalidNotifiableForUpdate` — raised by `UpdateWorker` when the supplied `notifiable_class` string is not `"Article"` or `"Comment"`.
- If the notifiable record no longer exists in the database when the worker runs, the worker returns early and the service is never called.
- If no `Notification` records match the given notifiable and action, the service exits without issuing any SQL write.
