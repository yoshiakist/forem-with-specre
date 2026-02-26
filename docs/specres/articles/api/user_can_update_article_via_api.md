---
id: "01KJCHPQSWKVZHSRRBZ4Q4KMNB"
name: "user_can_update_article_via_api"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/concerns/api/articles_controller.rb`
- `app/controllers/api/v0/articles_controller.rb`
- `app/controllers/api/v1/articles_controller.rb`
- `app/services/articles/updater.rb`
- `app/views/api/v0/articles/show.json.jbuilder`
- `app/views/api/v1/articles/show.json.jbuilder`
- `app/views/api/v0/articles/_article.json.jbuilder`
- `app/views/api/v1/articles/_article.json.jbuilder`
- `spec/requests/api/v0/articles_spec.rb` (Test)
- `spec/requests/api/v1/articles_spec.rb` (Test)
- `spec/requests/api/v1/docs/articles_spec.rb` (Test)
- `spec/services/articles/updater_spec.rb` (Test)

## Functional Overview

An authenticated API user can update an existing article by sending a PUT request to `/api/articles/:id`. Regular users may only update articles they own; super admins may update any article regardless of ownership. The request body accepts the same parameters as article creation. The update is delegated to `Articles::Updater`, which normalizes parameters, persists the changes, and triggers downstream side effects such as mention notifications, audience segment refresh, or notification removal depending on the article's publish state transition. On success the updated article representation is returned with HTTP 200; on validation failure a 422 error response is returned.

## Design Intent

Scoping the article lookup by `@user.articles` for regular users enforces row-level ownership at the query level, avoiding a separate authorization check and preventing information leakage via timing differences. Super admins bypass this scope via `Article.includes(:user)` to support moderation workflows. Delegating all update logic to `Articles::Updater` keeps the controller thin and makes the service independently testable. Parameter normalization (including `published_at` immutability once set) is centralized in `Articles::Attributes#for_update`, ensuring consistent behavior whether the request comes from v0 or v1.

## Key Members

- `PUT /api/articles/:id` — endpoint handled by the `update` action in the `Api::ArticlesController` concern, shared by v0 and v1 controllers
- `Articles::Updater.call(user, article, article_params)` — service object that performs the update and returns a `Result` struct with `success` and `article` fields
- `article_params` — permitted fields: `title`, `body_markdown`, `published`, `series`, `main_image`, `canonical_url`, `description`, `tags`, `published_at`, `subforem_id`, `language`, and conditionally `organization_id`, `video_source_url`, and admin-only `clickbait_score`, `compellingness_score`, `labels`
- `Result.success` — boolean indicating whether `article.update` persisted without errors
- `normalize_params` — strips `published_at` when the article is already published and not scheduled, and delegates further normalization to `Articles::Attributes#for_update`

## Scenarios

### Successful update by article owner

1. An authenticated user sends a PUT request to `/api/articles/:id` with one or more updatable fields.
2. The system looks up the article scoped to the requesting user's own articles.
3. `Articles::Updater` normalizes the parameters and calls `article.update`.
4. The article is persisted with the new values.
5. Side effects are triggered as appropriate (mentions created if article remains published, notifications removed if article was just unpublished, audience segments refreshed if article was just published for the first time).
6. The system responds with HTTP 200 and the full updated article representation.

### Super admin updates any article

1. A super admin sends a PUT request to `/api/articles/:id` where the article belongs to a different user.
2. The system looks up the article from the global `Article` scope (not scoped to the admin's own articles).
3. The update proceeds as normal and the article is saved.
4. The system responds with HTTP 200.

### Super admin updates admin-only fields

1. A super admin sends a PUT request including `clickbait_score`, `compellingness_score`, or `labels`.
2. These fields are included in the permitted parameters only for super admins.
3. The article is updated with those field values.
4. The system responds with HTTP 200.

### Non-admin attempts to update admin-only fields

1. A regular user sends a PUT request including `clickbait_score`, `compellingness_score`, or `labels`.
2. Those fields are excluded from the permitted parameters and silently ignored.
3. The remaining valid fields are processed normally.

### Article is published for the first time

1. A user updates a draft article with `published: true`.
2. `Articles::Updater` detects the transition from unpublished to published.
3. The user's auto audience segments are refreshed.
4. The system responds with HTTP 200.

### Article is unpublished

1. A user updates a published article with `published: false`.
2. `Articles::Updater` detects the transition from published to unpublished.
3. All existing "Published" notifications for the article, its comments, and its mentions are removed.
4. No new mention notifications are sent.
5. The system responds with HTTP 200.

### Article remains published after update

1. A user updates a published article without changing its published state.
2. `Articles::Updater` calls `Mentions::CreateAll` to create or update mentions in the article body.
3. The system responds with HTTP 200.

### Validation failure

1. A user sends a PUT request with invalid data (e.g., both `title` and `body_markdown` are nil).
2. `article.update` fails due to model validation errors.
3. The system responds with HTTP 422 and a JSON body containing `error` (a sentence summarizing the errors) and `status: 422`.

### Rate limit exceeded

1. A user sends a PUT request after exhausting their article update rate limit.
2. The rate limiter raises a rate limit error before the update is attempted.
3. The system responds with HTTP 429 and includes a `retry-after` header.

### Article not found or not owned

1. A regular user sends a PUT request for an article ID that does not exist or belongs to another user.
2. The scoped lookup raises a not-found error.
3. The system responds with HTTP 404.

### Request body is not a JSON object

1. A client sends a PUT request where the `article` parameter is not a hash/object.
2. The `validate_article_param_is_hash` check catches this before the update runs.
3. The system responds with HTTP 422 and an error message.

## Failures / Exceptions

- `published_at` is immutable once an article has been published (and is not currently scheduled); any `published_at` value in the request is silently dropped for already-published articles.
- `organization_id` is only permitted when the requesting user is a member of the target organization; non-members cannot assign or change the organization affiliation via the API.
- `video_source_url` is only permitted when the URL matches a YouTube, Mux, or Twitch pattern; other video URLs are silently ignored.
- When a super admin updates an article owned by another user, `edited_at` is still updated because the admin is treated as the acting user for the `update_edited_at` check.
