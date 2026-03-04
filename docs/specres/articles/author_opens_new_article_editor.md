---
id: "01KJV0FF10MZMWNFJB77RRFZ6S"
name: "author_opens_new_article_editor"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/articles_controller.rb`
- `app/services/articles/builder.rb`
- `app/models/article.rb`
- `app/javascript/article-form/articleForm.jsx`
- `app/javascript/packs/articleForm.jsx`
- `app/javascript/article-form/components/PageTitle.jsx`
- `app/views/articles/new.html.erb` (Template)
- `app/views/articles/_v2_form.html.erb` (Template)
- `app/views/articles/_quickie_form.html.erb` (Template)
- `spec/services/articles/builder_spec.rb` (Test)
- `spec/system/articles/user_creates_an_article_spec.rb` (Test)
- `app/javascript/article-form/components/__tests__/PageTitle.test.jsx` (Test)

## Functional Overview

When a user navigates to `/new`, the controller calls `Articles::Builder` with the current user, an optional tag, and an optional prefill string. `Builder#call` returns a `[Article, needs_authorization?]` pair. Unauthenticated visitors receive a registration form instead of the editor; authenticated users get the v2 editor shell rendered via `_v2_form.html.erb`, which embeds the article JSON in `data-article`. On mount, `ArticleForm` reads `localStorage` for `editor-v2-<url>` and, if the stored entry's `updatedAt` is newer than the server's `updated_at`, restores the draft fields (`title`, `tagList`, `bodyMarkdown`, `mainImage`, `videoSourceUrl`) into state.

## Design Intent

`Builder` centralises article-initialization logic and keeps the controller thin. The `needs_authorization?` boolean lets the controller skip Pundit for unauthenticated visitors (who cannot own an article) while still storing the target URL for post-login redirect. The localStorage restore ensures users do not lose work when they navigate away accidentally.

## Key Members

- `Articles::Builder#call` — returns `[Article, Boolean]`; dispatches to a private helper based on user, editor version, tag, and prefill
- `ArticleForm` constructor — parses server JSON, checks `localStorage`, and merges any newer draft into initial state via `previousContentState`
- `ArticleForm#componentDidMount` — registers `beforeunload` listener that calls `localStoreContent`

## Scenarios

### Unauthenticated visitor opens /new

1. Visitor navigates to `/new`.
2. Controller skips Pundit authorization and stores the target URL for post-login redirect.
3. Server renders a registration form in place of the editor.

### Authenticated user opens /new (v2 editor)

1. Signed-in user with editor v2 navigates to `/new`.
2. `Articles::Builder` returns an empty `Article` with `user_id` set; `needs_authorization?` is `false`.
3. Server renders `_v2_form.html.erb`, embedding article JSON in `data-article`.
4. `ArticleForm` mounts; if `localStorage` has a newer draft, it restores `title`, `tagList`, and `bodyMarkdown`.

### Editor restores unsaved draft from localStorage

1. User previously edited an article and navigated away (triggering `localStoreContent`).
2. User returns to the same editor URL.
3. `ArticleForm` constructor finds a stored entry whose `updatedAt` is newer than the server's `updated_at`.
4. Draft fields are spread into initial state; `edited` is set to `true`.

## Failures / Exceptions

- Suspended users are blocked by the `check_suspended` before-action and cannot reach `/new`.
- If `localStorage` is unavailable (private browsing with strict storage blocking), `JSON.parse(localStorage.getItem(...))` returns `null` and the form initializes from server data.
