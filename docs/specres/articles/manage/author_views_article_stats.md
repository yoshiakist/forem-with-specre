---
id: "01KJTZPRK0G09A0XZ3HREFQZT8"
name: "author_views_article_stats"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/articles_controller.rb`
- `app/models/article.rb`
- `app/policies/article_policy.rb`
- `app/views/articles/stats.html.erb` (Template)
- `app/javascript/packs/articlePage.jsx`
- `spec/requests/articles/articles_spec.rb` (Test)
- `spec/system/articles/user_visits_article_stats_spec.rb` (Test)
- `spec/policies/article_policy_spec.rb` (Test)

## Functional Overview

When an authenticated user navigates to an article's stats page (GET `/:username/:slug/stats`), the system verifies via `ArticlePolicy#stats?` that the requester is the article's author, an org admin of the article's organization, or a super admin. If authorized, the `stats` action loads the article's public reactions (up to 500, ordered by most recent) and the article's organization ID, then renders the `articles/stats` template. The template displays the article title as a link and delegates analytics rendering to a shared stats partial, while the `analyticsArticle` JavaScript pack handles chart display and API-driven data fetching on the client side.

## Scenarios

### Author successfully views stats

1. A signed-in user navigates to `/:username/:slug/stats` for their own article.
2. The `set_article` before-action locates the article by owner username and slug.
3. `ArticlePolicy#stats?` confirms the requester is the article's author and grants access.
4. The controller loads the most recent 500 public reactions with their associated users and records the article's organization ID.
5. The stats template renders, displaying the article title as a link and the shared stats partial; the `analyticsArticle` pack initializes analytics charts.

### Org admin views stats for an org article

1. A signed-in org admin navigates to the stats page of an article belonging to their organization.
2. `ArticlePolicy#stats?` recognizes the requester as an org admin of the article's organization and grants access.
3. The page renders with the article's stats data as in the normal author flow.

### Super admin views any article's stats

1. A signed-in super admin navigates to any article's stats page.
2. `ArticlePolicy#stats?` grants access based on the super admin role.
3. The page renders with the article's stats data.

### Unauthorized user is rejected

1. A signed-in user attempts to access the stats page of an article they did not author and for which they are not an org admin or super admin.
2. `ArticlePolicy#stats?` raises `Pundit::NotAuthorizedError`.
3. The application handles the error according to its standard authorization failure response.

## Failures / Exceptions

- Unauthenticated users are redirected to sign in by the `authenticate_user!` before-action (stats is not in the exemption list).
- Non-authors, non-org-admins, and non-super-admins receive a `Pundit::NotAuthorizedError` when the policy check fails.
