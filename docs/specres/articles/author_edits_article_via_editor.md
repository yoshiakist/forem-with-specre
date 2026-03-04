---
id: "01KJTZNTD1B2X40J6GGAH2K1ZK"
name: "author_edits_article_via_editor"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/articles_controller.rb`
- `app/models/article.rb`
- `app/policies/article_policy.rb`
- `app/services/articles/updater.rb`
- `app/services/articles/attributes.rb`
- `app/javascript/article-form/articleForm.jsx`
- `app/javascript/article-form/actions.js`
- `app/javascript/article-form/components/Form.jsx`
- `app/javascript/article-form/components/Header.jsx`
- `app/javascript/article-form/components/EditorActions.jsx`
- `app/javascript/article-form/components/EditorBody.jsx`
- `app/javascript/article-form/components/Title.jsx`
- `app/javascript/article-form/components/Meta.jsx`
- `app/javascript/article-form/components/Options.jsx`
- `app/javascript/article-form/components/Tabs.jsx`
- `app/javascript/article-form/components/Toolbar.jsx`
- `app/javascript/article-form/components/Close.jsx`
- `app/javascript/article-form/components/ErrorList.jsx`
- `app/javascript/packs/articleForm.jsx`
- `app/views/articles/edit.html.erb` (Template)
- `app/views/articles/_v2_form.html.erb` (Template)
- `spec/services/articles/updater_spec.rb` (Test)
- `spec/services/articles/attributes_spec.rb` (Test)
- `spec/requests/articles/articles_update_spec.rb` (Test)
- `spec/system/articles/user_edits_an_article_spec.rb` (Test)
- `spec/policies/article_policy_spec.rb` (Test)
- `spec/models/article_spec.rb` (Test)
- `app/javascript/article-form/components/__tests__/Form.test.jsx` (Test)
- `app/javascript/article-form/components/__tests__/Options.test.jsx` (Test)

## Functional Overview

When an authenticated, non-suspended author navigates to an article's edit page, the server renders a React-based editor (v1 for front-matter articles, v2 for the rich form) seeded with the article's current data. The frontend `ArticleForm` component manages all editor state, persists unsaved work to localStorage, and submits changes via a `PUT /articles/:id` JSON request. The controller delegates attribute normalization to `Articles::Attributes#for_update` and persistence to `Articles::Updater`, which enforces rate limits, updates the article, then fires post-save side-effects (mention notifications, audience-segment refresh, notification cleanup) based on the resulting published-state transition.

## Key Members

- `Articles::Updater#call` — rate-checks, saves, dispatches post-save side-effects based on publish-state transition
- `Articles::Attributes#for_update` — whitelists and normalizes attributes; resolves `series` to a `Collection`; stamps `edited_at` when requested
- `submitArticle` — chooses PUT vs POST based on presence of `payload.id`; redirects to `current_state_path` on success
- `ArticleForm#localStoreContent` — saves editor state to `localStorage` keyed by editor version and URL on `beforeunload`
- `article_params_json` — permits different param sets for v1 (body_markdown only) vs v2 (full field list); conditionally allows `organization_id`, `user_id`, and `co_author_ids_list`

## Scenarios

### Author opens the edit page

1. Author navigates to `/:username/:slug/edit`; `ArticlesController#edit` authenticates and authorizes via `ArticlePolicy`
2. Controller determines editor version: v1 if the article has front-matter, v2 otherwise
3. The `edit.html.erb` template renders the `_v2_form` partial, which embeds article JSON in `data-article` on the `<main>` element
4. The `articleForm` JS pack mounts `ArticleForm`, which reads the data attribute, checks localStorage for a newer unsaved draft, and initializes component state accordingly

### Author edits and saves changes

1. Author modifies the title, body, tags, cover image, or other fields in the editor
2. Any input event sets `edited: true` in component state and triggers localStorage persistence via `localStoreContent`
3. Author clicks "Save changes" (publish) or "Save draft"; `onPublish` or `onSaveDraft` sets `submitting: true` and calls `submitArticle` with the current state and the appropriate `published` flag
4. `submitArticle` sends `PUT /articles/:id` with the serialized payload; the controller calls `Articles::Updater.call`
5. On success, the browser is redirected to `current_state_path` and localStorage is cleared; on error, validation messages are displayed at the top of the form

### Author publishes a previously unpublished article

1. Author sets or confirms `published: true` in the editor and submits
2. `Articles::Updater` detects the `became_published?` transition and calls `user.refresh_auto_audience_segments`
3. Mention and follower notifications are dispatched via `Mentions::CreateAll`

### Author unpublishes a published article

1. Author sets `published: false` in the editor and submits
2. `Articles::Updater` detects `became_unpublished?` and removes all existing published-action notifications and related comment/mention notifications

### Author exceeds the rate limit

1. Author attempts to save but `user.rate_limiter.check_limit!(:article_update)` raises a rate-limit error
2. The error propagates back to the controller, which returns an unprocessable-entity response
3. The editor displays a "Rate limit reached" error to the author

## Failures / Exceptions

- Invalid article attributes (e.g., blank title) cause `article.update` to return false; the controller responds with 422 and the article's validation errors as JSON
- Rate limit exceeded raises before the update is attempted; the editor surfaces the error message
- Unauthorized access (non-owner, suspended user) is rejected by `ArticlePolicy` or the `check_suspended` before-action, resulting in a 403/redirect
