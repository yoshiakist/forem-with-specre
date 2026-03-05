---
id: "01KJCHJFD7KGAQSDCCXMC9W7WY"
name: "user_can_create_article_via_api"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/concerns/api/articles_controller.rb`
- `app/controllers/api/v0/articles_controller.rb`
- `app/controllers/api/v1/articles_controller.rb`
- `app/services/articles/creator.rb`
- `app/views/api/v0/articles/show.json.jbuilder`
- `app/views/api/v1/articles/show.json.jbuilder`
- `app/views/api/v0/articles/_article.json.jbuilder`
- `app/views/api/v1/articles/_article.json.jbuilder`
- `spec/requests/api/v0/articles_spec.rb` (Test)
- `spec/requests/api/v1/articles_spec.rb` (Test)
- `spec/requests/api/v1/docs/articles_spec.rb` (Test)
- `spec/services/articles/creator_spec.rb` (Test)

## Functional Overview

An authenticated user can create a new article by sending a POST request to `POST /api/articles`. In API v0, authentication is performed via session or API key; in API v1, an API key is required. The request body must be a JSON object with the article parameters nested under an `article` key. The system delegates creation to `Articles::Creator`, which enforces rate limits, creates the article record, optionally assigns it to a series (collection), subscribes the author to comment notifications, and refreshes audience segments if the article is published. On success, the response returns HTTP 201 Created with the article JSON and a `Location` header pointing to the article URL. On validation failure, the response returns HTTP 422 with an error message.

## Design Intent

The `create` action lives in the `Api::ArticlesController` concern so it is shared between v0 and v1 controllers without duplication. Authentication strategy differs by version — v0 uses session-based `authenticate!` while v1 uses `authenticate_with_api_key!` — but the creation logic itself is version-agnostic. `Articles::Creator` is extracted as a service object to keep the controller thin and to centralise rate limiting, series resolution, and post-creation side effects.

## Key Members

- `article_params` — permitted parameters: `title`, `body_markdown`, `published`, `series`, `main_image`, `canonical_url`, `description`, `tags` (array), `published_at`, `subforem_id`, `language`. Additionally `organization_id` (if the user is an org member), `video_source_url` (if the URL matches YouTube, Mux, or Twitch patterns), and `clickbait_score`, `compellingness_score`, `labels` (super admins only).
- `Articles::Creator` — service object accepting the current user and the article params. Applies rate limiting, creates the `Article` record, resolves the series, creates a `NotificationSubscription` for the author, and triggers audience segment refresh on publication.
- `NotificationSubscription` — created with `config: "all_comments"` so the author is notified of every comment on the new article.

## Scenarios

### Successful article creation (unpublished by default)

1. Authenticated user sends `POST /api/articles` with a JSON body containing at least a `title` under the `article` key.
2. System authorizes the action via `ArticlePolicy`.
3. `Articles::Creator` enforces the rate limit (stricter limit for new users).
4. A new `Article` record is created, assigned to the requesting user, with `show_comments` set to true.
5. If a `series` parameter is provided, the article is linked to the matching or newly created `Collection`.
6. A `NotificationSubscription` is created so the author receives notifications for all comments.
7. System responds with HTTP 201 Created, the article JSON body, and a `Location` header pointing to the article URL.
8. The article is unpublished (`published: false`) unless `published: true` was explicitly passed.

### Successful article creation (published immediately)

1. Authenticated user sends `POST /api/articles` with `published: true` and a valid `title`.
2. Steps 2–6 from the default scenario apply.
3. Because the article is published, `user.refresh_auto_audience_segments` is called asynchronously.
4. System responds with HTTP 201 Created.

### Article creation with front matter in the body

1. Authenticated user sends `POST /api/articles` with `body_markdown` containing YAML front matter (title, published, tags, etc.) but no explicit top-level title parameter.
2. The article's attributes are resolved from the front matter during processing.
3. System responds with HTTP 201 Created and the article reflects the values from the front matter.

### Article creation within an organization series

1. Authenticated org-member sends `POST /api/articles` with `organization_id` and `series` parameters.
2. System checks org membership before permitting `organization_id`.
3. `Articles::Creator` looks up or creates a `Collection` scoped to the given organization and series slug.
4. The new article is linked to that collection.
5. System responds with HTTP 201 Created.

## Failures / Exceptions

- **401 Unauthorized** — request is missing or provides an invalid API key, the user is suspended, or site policy restricts creation to admins only.
- **422 Unprocessable Entity** — article params are not wrapped under the `article` key, params are not a JSON object (e.g., a string), required fields are missing, or validation fails (e.g., tags contain non-alphanumeric characters, body markdown is blank when a title from front matter is present).
- **429 Too Many Requests** — the user has exceeded the article creation rate limit; the response includes a `retry-after` header.
