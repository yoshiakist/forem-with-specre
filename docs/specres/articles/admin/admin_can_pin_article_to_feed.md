---
id: "01KJBWMN1X7QK4TMQ77F5NFR6E"
name: "admin_can_pin_article_to_feed"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/models/pinned_article.rb`
- `app/controllers/stories/pinned_articles_controller.rb`
- `app/controllers/admin/articles_controller.rb`
- `app/javascript/admin/controllers/article_pinned_modal_controller.js`
- `app/policies/pinned_article_policy.rb`
- `app/validators/existing_published_article_id_validator.rb`
- `app/views/admin/articles/_pinned_article_modal.html.erb` (Template)
- `spec/models/pinned_article_spec.rb` (Test)
- `spec/requests/stories/pinned_articles_spec.rb` (Test)
- `spec/policies/pinned_article_policy_spec.rb` (Test)

## Functional Overview

Admins and super-admins can designate exactly one published article to be pinned at the top of the site feed at any given time. The pinned article ID is stored in `Settings::General` so only one article can be pinned simultaneously. Pinning is performed either through the admin articles UI (which shows a confirmation modal when another article is already pinned) or through a dedicated JSON API used by the admin front-end. Both surfaces require admin-level authorization enforced by `PinnedArticlePolicy`. All pin and unpin actions are recorded in the moderator audit log.

## Design Intent

Only a single global pinned article is supported, stored as a settings value rather than a database record, which means pinning a new article automatically replaces any previously pinned one with no need for explicit cleanup logic. The `PinnedArticle` module wraps all access to this setting and guards against returning stale IDs for articles that have since been unpublished or deleted.

## Key Members

- `Settings::General.feed_pinned_article_id` — the persisted ID of the currently pinned article; `nil` when nothing is pinned
- `PinnedArticle.get` — returns the live `Article` record, or `nil` if the setting is absent, the article has been deleted, or the article has been unpublished

## Scenarios

### Admin pins an article via the API

1. An admin sends a PUT request to the pinned-article endpoint with the target article's ID.
2. The system verifies the requester is authenticated and has admin privileges.
3. The system looks up the article and confirms it is published.
4. The system records the article's ID as the globally pinned article, replacing any previously pinned one.
5. The action is written to the moderator audit log and a 204 response is returned.

### Admin reads the currently pinned article via the API

1. An admin sends a GET request to the pinned-article endpoint.
2. The system returns a JSON object containing the article's ID, URL path, title, and the timestamp when it was last pinned.
3. If no article is currently pinned, the system responds with 404 and a not-found error message.

### Admin unpins an article via the API

1. An admin sends a DELETE request to the pinned-article endpoint.
2. The system clears the pinned article setting.
3. The action is written to the moderator audit log and a 204 response is returned.

### Admin pins an article through the admin UI

1. An admin navigates to the admin articles view and clicks the pin action for an article.
2. If another article is already pinned, the browser displays a confirmation modal showing the currently pinned article's title and pinned date, and asks the admin to confirm replacement.
3. After confirmation (or immediately if nothing is pinned), the form is submitted.
4. The server pins the selected article, sets a success flash message, and redirects to the article's admin detail page.

### Admin unpins an article through the admin UI

1. An admin triggers the unpin action for an article in the admin UI.
2. The server clears the pinned article setting, sets a danger flash message, and redirects to the article's admin detail page.

## Failures / Exceptions

- Unauthenticated requests to the API receive a 401 response.
- Authenticated non-admin users receive a `Pundit::NotAuthorizedError`.
- A PUT request referencing a non-existent article ID or a draft (unpublished) article receives a 422 response with an error message.
- `PinnedArticle.exists?`, `.id`, and `.get` return `false` or `nil` when the stored article ID refers to an article that has since been deleted or unpublished.
