---
id: "01KJ9R5SGS1KVY0NHAXT8H5WNJ"
name: "system_resaves_user_articles"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/workers/users/resave_articles_worker.rb`
- `spec/workers/users/resave_articles_worker_spec.rb` (Test)

## Functional Overview

When the system needs to propagate changes affecting a user's articles (for example, after a profile update), it enqueues `Users::ResaveArticlesWorker` with the user's ID. The worker looks up the user by ID, and if found, iterates over all of the user's articles and re-saves each one. This triggers any `before_save` or `after_save` callbacks on the article model, ensuring that derived data, caches, or external integrations are refreshed. The job runs on the medium-priority queue with a concurrency limit of one and will retry up to ten times on failure.

## Design Intent

The concurrency limit of one prevents multiple simultaneous resave jobs for the same worker class from hammering the database, protecting system stability during bulk operations.

## Scenarios

### System resaves all articles for an existing user

1. The system enqueues the worker with a valid user ID.
2. The worker locates the user in the database.
3. The worker iterates over every article belonging to that user and saves each one, triggering all model callbacks.
4. Each article's state and any associated caches or integrations are refreshed.

### System skips processing when the user does not exist

1. The system enqueues the worker with a user ID that does not match any record (e.g., a nil or deleted-user ID).
2. The worker attempts to find the user and receives no result.
3. The worker exits immediately without raising an error or processing any articles.
