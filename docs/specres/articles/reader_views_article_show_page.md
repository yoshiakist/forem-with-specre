---
id: "01KJCK5NSKJNEBDJYZA4QQ3YBW"
name: "reader_views_article_show_page"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/stories_controller.rb`
- `app/decorators/article_decorator.rb`
- `app/helpers/articles_helper.rb`
- `app/views/articles/show.html.erb`
- `app/views/articles/_actions.html.erb`
- `app/views/articles/_full_comment_area.html.erb`
- `app/views/articles/_comment_tree.html.erb`
- `app/views/articles/_comments_actions.html.erb`
- `app/views/articles/_conduct_and_abuse_actions.html.erb`
- `app/views/articles/_multiple_engagements.html.erb`
- `app/views/articles/_multiple_reactions.html.erb`
- `app/views/articles/_multireaction_button.html.erb`
- `app/views/articles/_reaction_button.html.erb`
- `app/views/articles/_reaction_category_resources.html.erb`
- `app/javascript/packs/articlePage.jsx`
- `app/javascript/packs/articleSignedIn.jsx`
- `app/javascript/packs/localizeArticleDates.js`
- `app/javascript/packs/articleAnimations.jsx`
- `app/javascript/common-prop-types/article-prop-types.js`
- `spec/requests/articles/articles_show_spec.rb` (Test)
- `spec/requests/stories_show_spec.rb` (Test)
- `spec/requests/stories_performance_fix_spec.rb` (Test)
- `spec/decorators/article_decorator_spec.rb` (Test)
- `spec/helpers/articles_helper_spec.rb` (Test)

## Functional Overview

When a reader navigates to an article URL (`/:username/:slug`), `StoriesController#show` resolves the article by its path with the user preloaded, then delegates to `handle_article_show`. That method calls `assign_article_show_variables`, which enforces access control (unpublished and scheduled articles require the author's preview password), gates spam-author articles to admins only, and then loads all data the view needs: the author, optional organization, discussion lock state, collection and ordered collection articles, co-authors, comments count, sort order, and a context note. After setting surrogate-cache keys for CDN invalidation, the controller renders `articles/show`, which emits a three-column layout containing a left-sidebar actions bar (reactions, share, moderation), a main content area (cover image or video, author byline, publication date, tags, processed article body, optional series navigator, and comment section), and a right sidebar with sticky navigation. JavaScript packs initialize the share dropdown, copy-link button, comment subscription widget, fullscreen code mode, animated-image controls, and lazy-loaded bottom content.

## Design Intent

The controller separates route resolution (`show`), permission and redirect logic (`handle_article_show`), and variable assignment (`assign_article_show_variables`) so each concern is independently testable and cacheable. Surrogate-key headers are set before any redirect is checked so CDN purge granularity is preserved even on redirect responses. The `ArticleDecorator` wraps display-only logic (title classification, co-author link generation, `long_markdown?` threshold) to keep the model and view free of presentation coupling.

## Key Members

- `@article` — the decorated `Article` record, resolved by `/username/slug` path
- `@user` — the article's author, used for byline, profile image, and JSON-LD
- `@organization` — optional; when present, the org avatar overlays the author avatar
- `@discussion_lock` — when set, suppresses the comment form and shows a lock reason
- `@collection` / `@collection_articles` — series data, rendered when the article belongs to a collection
- `@comments_to_show_count` — 50 for `discuss`-tagged articles, 30 otherwise; reduced to 10 for signed-out readers
- `@comments_order` — `"top"` by default; overridable via `?comments_sort=` for signed-in users

## Scenarios

### Reader views a published article

1. Reader requests `/:username/:slug`.
2. Controller finds the article by path (including the user association) and decorates it.
3. `assign_article_show_variables` confirms the article is published and the author is not a spam user (admins still gain access).
4. Author, organization, collection, discussion lock, and comment metadata are assigned.
5. The view renders the three-column layout: cover image or video, author byline with publication date, tags, article body, and comment section.
6. JavaScript packs are loaded to wire up the share dropdown, copy-link button, comment subscription, and bottom-content lazy loader.

### Reader visits an article with a changed or organization-owned path

1. Reader requests an old `/:username/:slug` path where the article has moved to an organization or the author changed their username.
2. `show` finds the article by slug alone, detects the mismatch, and issues a `301 Moved Permanently` redirect to the canonical path.
3. The `?i=i` internal-navigation parameter is preserved if present in the original request.

### Author or admin previews an unpublished or scheduled article

1. The requester visits the article path with a `?preview=<password>` query parameter.
2. `permission_denied?` returns false because the preview token matches the article's password.
3. `assign_article_show_variables` proceeds normally; the view displays a danger notice banner indicating the article is unpublished or a warning banner indicating it is scheduled.
4. An "Edit" link is revealed client-side if the viewer is the author.

### Reader views an article with a discussion lock

1. An article's `discussion_lock` association is present.
2. The comment form is suppressed; instead, the lock-reason partial is rendered in the comment area.
3. The existing comment tree is still displayed.

### Signed-out reader encounters comment filtering

1. Reader requests an article without being signed in.
2. `@comments_to_show_count` is capped at 10.
3. Only comments with a non-negative score are shown; all negative-score comments are hidden.
4. A "View full discussion" link is shown when the article's `displayed_comments_count` exceeds the cap.

## Failures / Exceptions

- If the article is not found by path or slug, and no matching podcast episode or page exists, `not_found` is raised (404).
- If `params[:slug]` contains characters that `Article.includes(:user).find_by` cannot parse, an `ArgumentError` is rescued and returned as `400 Bad Request`.
- If the author has the `spam` role and the requesting user is not an admin, `not_found` is raised (404) regardless of publication state.
- If the article belongs to a subforem that does not match the current request context, a `301` redirect to the canonical subforem URL is issued.
