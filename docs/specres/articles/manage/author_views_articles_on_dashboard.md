---
id: "01KJV3PD89JNE8190FG9GCAV33"
name: "author_views_articles_on_dashboard"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/dashboards_controller.rb`
- `app/models/article.rb`
- `app/policies/article_policy.rb`
- `app/decorators/article_decorator.rb`
- `app/views/dashboards/show.html.erb` (Template)
- `app/views/dashboards/_dashboard_article.html.erb` (Template)
- `app/views/dashboards/_dashboard_article_row.html.erb` (Template)
- `app/views/dashboards/_header_and_action.html.erb` (Template)
- `app/javascript/packs/archivedPostFilters.js`
- `app/javascript/packs/dashboardDropdowns.js`
- `app/javascript/packs/dashboards/convertCoauthorIdsToUsernameInputs.js`
- `app/javascript/packs/initializers/initializeDashboardSort.js`
- `app/javascript/packs/initializers/__tests__/initializeDashboardSort.test.js` (Test)
- `spec/requests/dashboard_spec.rb` (Test)
- `spec/views/dashboards/show.html.erb_spec.rb` (Test)
- `spec/system/dashboards/user_sorts_dashboard_articles_spec.rb` (Test)

## Functional Overview

When an authenticated author visits `/dashboard`, the system loads their articles scoped to the current subforem and displays them as a paginated list (25 per page). By default, the list shows full posts sorted by creation date descending; passing `state=status` switches to status-type posts instead. Each article row shows its publication state — published, draft, or scheduled — along with engagement stats (reactions, comments, page views) for published articles and a delete or manage action. The list can be re-sorted by creation date, views, reactions, comments, or publish date via a `sort` query parameter. Organization admins may switch between their personal articles and an organization's articles using a dropdown. If a user has no existing articles and cannot create new ones, they are redirected to the following-tags page.

## Design Intent

The `has_existing_articles_or_can_create_new_ones?` policy method gates entry to the dashboard: authors who have never published and lack create permission are silently redirected rather than shown an empty list. Aggregate counts (reactions, comments, page views) are computed before decoration and pagination so the totals reflect the full unfiltered result set. Articles are decorated before pagination so that `ArticleDecorator#current_state` and `#current_state_path` are available inside the view partials.

## Key Members

- `params[:state]` — when set to `"status"`, applies the `Article.statuses` scope; otherwise applies `Article.full_posts`
- `params[:sort]` — passed to `Article.sorting/1`; accepted values are `creation-asc`, `creation-desc`, `views-asc`, `views-desc`, `reactions-asc`, `reactions-desc`, `comments-asc`, `comments-desc`, `published-asc`, `published-desc`; defaults to `creation-desc`
- `params[:org_id]` + `params[:which]` — when `which=organization` and the user is an org admin, loads articles belonging to that organization instead of the current user
- `ARTICLES_PER_PAGE` — constant set to 25, controls Kaminari pagination

## Scenarios

### Author views dashboard with a mix of published and draft articles

1. Authenticated user navigates to `/dashboard`.
2. The controller loads the user's full posts for the current subforem, sorted by creation date descending.
3. Each article row shows the article title and a state badge: "Draft" for unpublished articles, "Scheduled" for articles with a future publish date, or no badge for published articles.
4. Published articles display reactions count, comments count, and page views.
5. Draft articles owned by the user show a Delete button; published articles show a Manage link and a Stats link.

### Author filters dashboard to show only status posts

1. Authenticated user navigates to `/dashboard?state=status`.
2. The controller applies the `statuses` scope, returning only articles of `type_of: :status`.
3. The view renders the filtered list; the "Statuses" toggle button changes to a "Full" button to allow switching back.
4. Aggregate totals (reactions, comments, page views) reflect the filtered set.

### Author sorts articles by different criteria

1. Authenticated user navigates to `/dashboard?sort=<value>` where `<value>` is one of `creation-asc`, `views-desc`, `reactions-asc`, `comments-desc`, or `published-desc`.
2. The `Article.sorting` scope maps the parameter to the corresponding `ORDER BY` clause.
3. The dashboard re-renders with articles in the requested order.
4. The sort dropdown in the UI reflects the active sort value.

### Author switches between personal and organization article views

1. An authenticated org admin navigates to `/dashboard`.
2. An organization dropdown appears if the user belongs to one or more organizations.
3. Selecting an organization navigates to `/dashboard/organization/<org_id>`.
4. The controller verifies org admin membership, then loads and displays that organization's articles without the state filter or sort dropdown.
5. Each article row in the organization view shows the author's avatar and allows co-author management.

### Author with no articles sees empty state

1. Authenticated user with no articles and no article-creation permission navigates to `/dashboard`.
2. The `has_existing_articles_or_can_create_new_ones?` policy check returns false.
3. The controller redirects the user to `/dashboard/following_tags`.
4. If the user can create articles but simply has none yet, the empty state card is shown with a "Write your first post" link.

## Failures / Exceptions

- Non-org-admin users who request `/dashboard/organization/<org_id>` receive a `Pundit::NotAuthorizedError`.
- Unauthenticated requests to `/dashboard` are redirected to `/magic_links/new` by `authenticate_user!`.
