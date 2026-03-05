---
id: "01KJV0FFF2JMT324JSMKPFW9Z3"
name: "author_submits_new_article"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/articles_controller.rb`
- `app/services/articles/creator.rb`
- `app/models/article.rb`
- `app/policies/article_policy.rb`
- `app/javascript/article-form/actions.js`
- `app/javascript/article-form/components/EditorActions.jsx`
- `app/javascript/article-form/components/Header.jsx`
- `spec/services/articles/creator_spec.rb` (Test)
- `spec/requests/articles/articles_create_spec.rb` (Test)
- `spec/policies/article_policy_spec.rb` (Test)
- `spec/models/article_spec.rb` (Test)

## Functional Overview

When the author clicks "Publish" or "Save draft", `EditorActions` calls `onPublish` or `onSaveDraft` on `ArticleForm`, which sets `published: true/false`, marks `submitting: true`, and calls `submitArticle`. `submitArticle` in `actions.js` chooses `POST /articles` (when there is no `payload.id`) and sends the article payload as JSON. The controller authorizes via Pundit, then delegates to `Articles::Creator`. `Creator` checks the rate limit, creates the `Article` record with `show_comments: true`, resolves the `series` param into a `Collection`, subscribes the author to all-comment notifications, and enqueues `SegmentedUserRefreshWorker` if the article is published. On success the controller returns `{ id, current_state_path }` and the browser navigates to the article.

## Design Intent

`submitArticle` uses the presence of `payload.id` to decide between POST and PUT, making the same function reusable for both create and update. `Articles::Creator` separates persistence logic from the controller, handling rate limiting, series resolution, and post-save side effects (notifications, audience segments) in one place.

## Key Members

- `submitArticle(payload, onSuccess, onError)` — POSTs to `/articles`; calls `onSuccess({ id, current_state_path })` or `onError(errors)`
- `EditorActions` — renders "Publish" / "Save draft" / "Save changes" buttons; shows a disabled spinner while `submitting` is true
- `Articles::Creator#call` — calls `rate_limit!`, `create_article`, `subscribe_author`, and conditionally `refresh_auto_audience_segments`

## Scenarios

### Author publishes a new article

1. Author clicks "Publish" in `EditorActions`.
2. `ArticleForm` sets `published: true`, `submitting: true`, and calls `submitArticle`.
3. `submitArticle` POSTs the payload to `/articles`.
4. Controller authorizes and delegates to `Articles::Creator`.
5. `Creator` checks rate limit, creates the article with `show_comments: true`, and subscribes the author to all-comment notifications.
6. `SegmentedUserRefreshWorker` is enqueued for the author.
7. Controller returns `{ id, current_state_path }`; browser navigates to the article.

### Author saves a new article as draft

1. Author clicks "Save draft" in `EditorActions`.
2. `ArticleForm` sets `published: false` and calls `submitArticle`.
3. Steps 3–5 proceed as above, but without enqueuing `SegmentedUserRefreshWorker`.
4. Browser navigates to the article's draft URL.

## Failures / Exceptions

- `RateLimitChecker` raises `TooManyRequests`; controller renders HTTP 429 with a `Retry-After` header.
- Invalid article attributes leave the `Article` unpersisted; controller serializes `article.errors` as JSON with HTTP 422.
- Suspended users are blocked before reaching `create`.
