---
id: "01KJTZEM8AT0EMBHCD6T08T9PW"
name: "admin_views_and_updates_articles_in_admin_panel"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/admin/articles_controller.rb`
- `app/javascript/admin/controllers/article_controller.js`
- `app/views/admin/articles/index.html.erb` (Template)
- `app/views/admin/articles/show.html.erb` (Template)
- `app/views/admin/articles/_article_item.html.erb` (Template)
- `app/views/admin/articles/_image_upload_script.html.erb` (Template)
- `app/views/admin/users/show/articles/_index.html.erb` (Template)
- `spec/requests/admin/articles_spec.rb` (Test)
- `spec/requests/articles/articles_admin_feature_spec.rb` (Test)
- `app/javascript/admin/__tests__/controllers/article_controller.test.js` (Test)

## Functional Overview

The admin articles panel allows privileged administrators to browse published articles in multiple sort orders (hot/mixed by hotness score, chronological, or top articles over a time window), view an individual article's details including privileged reaction counts and moderation flags, and update article attributes such as featured status, approved status, email digest eligibility, author, co-authors, max score, published-at timestamp, and social image. Each update is recorded in the audit log. Administrators can also pin a single article to the top of the feed or remove an existing pin; pin/unpin actions support both full-page and Ajax (JS) responses and coordinate with a Stimulus-driven confirmation modal when replacing an existing pin. A separate Stimulus controller (`ArticleController`) manages client-side interactions such as adjusting a featured-number input value and visually highlighting a card after an action.

## Design Intent

Audit logging is applied via `after_action` on `update` and `unpin` so that every modification to article state is traceable to the acting moderator. The pinned article is excluded from the main article list query to avoid duplication in the index view. The `pinArticle` client-side action fetches the current pinned article before submitting so that a confirmation modal can warn the admin when displacing an already-pinned article, preventing accidental replacement without acknowledgment.

## Key Members

- `ARTICLES_ALLOWED_PARAMS` — whitelist of article attributes an admin may update; prevents mass-assignment of non-approved fields
- `@countable_vomits` — hash mapping article ID to the count of non-invalid "vomit" privileged reactions; surfaced in article cards as a flag count
- `@pinned_article` — the currently pinned article retrieved via `PinnedArticle.get`; excluded from the main listing and rendered separately at the top

## Scenarios

### Browsing articles in the admin panel

1. An admin navigates to the admin articles index.
2. Without a state parameter the system returns articles ordered by hotness score (mixed view) and separately loads manually featured upcoming articles.
3. With `state=chronological` the system returns published articles ordered by published date descending.
4. With a `state=top-N` parameter the system returns published articles from the last N months ordered by public reaction count descending.
5. The pinned article (if any) is displayed in a dedicated section above the list and excluded from the main paginated results.

### Viewing a single article in the admin panel

1. An admin navigates to the detail page for a specific article.
2. The system loads the article along with its reactions and associated user.
3. The page displays article metadata, status indicators (pinned, featured, approved, video, user warned), reaction counts (thumbsup, thumbsdown, vomit flags, overall score), moderation actions, and an editable attribute form.
4. On the individual article view, privileged reactions are split into flag (vomit) and quality reaction tabs.

### Updating article attributes

1. An admin submits the article edit form with changes to allowed fields (featured, approved, email digest eligibility, author, co-authors, max score, published-at, social image).
2. The system applies the update with the `admin_update` flag set to true.
3. On success the admin is redirected back to the article detail page with a success flash message.
4. On failure the admin is redirected back with a danger flash message containing the validation errors.
5. An audit log entry is created recording the moderator and the submitted parameters.

### Pinning an article

1. An admin clicks the pin button on an article card.
2. The `ArticleController` Stimulus controller intercepts the form submission and first fetches the currently pinned article via the feed endpoint.
3. If another article is already pinned, an `article-pinned-modal:open` event is dispatched, opening a confirmation modal that lets the admin confirm or cancel the pin replacement.
4. If no article is currently pinned (404 response) or the admin is re-pinning the same article, the pin form submits directly.
5. The server sets the article as the pinned article and responds with a redirect (HTML) or a re-rendered article partial (JS/Ajax).

### Unpinning an article

1. An admin clicks the unpin button on a pinned article card.
2. The `ArticleController` intercepts and immediately submits the unpin form.
3. The server removes the pinned article record and responds with a redirect to the article detail page (HTML) or a re-rendered article partial (Ajax).
4. An audit log entry is created.

## Failures / Exceptions

- If the article ID does not exist during unpin, the server raises `ActiveRecord::RecordNotFound` (404).
- If an article update fails validation, the controller redirects back to the article detail page with a danger flash message containing the errors as a sentence rather than raising an exception.
