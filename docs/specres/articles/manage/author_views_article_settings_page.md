---
id: "01KJTZP36VCPRDPVFG9EB99APB"
name: "author_views_article_settings_page"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/articles_controller.rb`
- `app/models/article.rb`
- `app/policies/article_policy.rb`
- `app/decorators/article_decorator.rb`
- `app/views/articles/manage.html.erb` (Template)
- `spec/requests/articles/articles_spec.rb` (Test)

## Functional Overview

When an author navigates to `/:username/:slug/manage`, the system renders a management hub page for a published, non-scheduled article. The controller authorizes the request via `ArticlePolicy#manage?`, which requires the current user to satisfy `update?` (author, org admin, or any admin) and further restricts access to articles that are both published and not scheduled. The article is decorated with `ArticleDecorator` before the view renders. The page presents a sidebar-navigated layout with sections for: Post Overview (title, organization, series, publish/edit dates, tags, org-admin author change form), Statistics (page views, reactions, comments counts with a link to the detailed stats page), Edit Post link, Pin to Profile (using `ProfilePin`, up to 5 pins), Discussion Lock (lock/unlock links to confirmation pages), Delete Post (link to delete confirmation with a permanent-deletion warning), and promotional Tips.

## Design Intent

Access is gated to published, non-scheduled articles only (`manage?` policy). Drafts and scheduled articles are explicitly excluded to keep the management surface focused on live content. The decorator pattern separates presentation logic (state path, tag array, readable dates) from the model, keeping the view and controller clean.

## Key Members

- `@article` — decorated `ArticleDecorator` wrapping the found article; provides `current_state_path`, `cached_tag_list_array`, `readable_publish_date`, `profile_pins`, `pinned?`
- `@discussion_lock` — the associated `DiscussionLock` record (or nil) controlling lock/unlock UI
- `@org_members` — list of `[name, id]` pairs for the organization's users; present only when the current user is an org admin of the article's organization

## Scenarios

### Author successfully views the management page

1. A signed-in user navigates to the manage path of their own published, non-scheduled article.
2. The controller calls `set_article` to locate the article, then authorizes via `ArticlePolicy#manage?`.
3. The article is decorated and the discussion lock, user, and organization members are assigned.
4. The page renders with sections for overview, statistics, edit, pin, discussion lock, delete, and tips.
5. The response is HTTP 200 and the page includes "Manage Your Post".

### Access denied for a draft article

1. A signed-in user navigates to the manage path of a draft (unpublished) article they own.
2. `ArticlePolicy#manage?` returns false because `record.published?` is false.
3. Pundit raises `Pundit::NotAuthorizedError` and the request is rejected.

### Access denied for a scheduled article

1. A signed-in user navigates to the manage path of an article set to publish in the future.
2. `ArticlePolicy#manage?` returns false because `record.scheduled?` is true.
3. Pundit raises `Pundit::NotAuthorizedError` and the request is rejected.

### Access denied for a non-author

1. A signed-in user navigates to the manage path of another user's published article.
2. `ArticlePolicy#manage?` delegates to `update?`, which checks `user_author?` and admin roles; none apply.
3. Pundit raises `Pundit::NotAuthorizedError` and the request is rejected.

### Organization admin can change the article's author

1. On the management page, when the current user is an org admin of the article's organization, a "Change Author" form is displayed in the overview section.
2. The form populates a select menu with all members of the organization (`@org_members`).
3. Submitting the form calls the update action with the new `user_id`, reassigning authorship within the organization.
