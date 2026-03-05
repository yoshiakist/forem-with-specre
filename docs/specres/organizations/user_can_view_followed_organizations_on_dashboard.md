---
id: "01KHZGV8H4BG6XE1A7T06AVD4X"
name: "user_can_view_followed_organizations_on_dashboard"
status: "draft"
---

## Related Files

- `app/views/dashboards/following_organizations.html.erb`
- `app/controllers/dashboards_controller.rb`

## Functional Overview

Authenticated users can navigate to the dashboard's followed organizations page to see a list of every organization they follow. The page fetches all `Organization` follows for the current user (or an admin-specified user), ordered by most recently followed, and renders each as a card showing the organization's logo, name, and username. When the user follows no organizations, a localized empty-state message is displayed instead of the grid.

## Scenarios

### Viewing followed organizations when follows exist

1. An authenticated user navigates to the followed organizations section of their dashboard.
2. The controller's `following_organizations` action authorizes the user via `fetch_and_authorize_user` and loads all follows of type `Organization` for that user, ordered by most recently followed first.
3. The view renders a responsive grid of organization cards.
4. Each card displays the organization's logo image, its display name as a link to the organization's profile, and its `@username` as a secondary link.

### Viewing followed organizations when no follows exist

1. An authenticated user navigates to the followed organizations section of their dashboard but has not followed any organizations.
2. The controller loads an empty collection for `@followed_organizations`.
3. The view renders a full-width empty-state card with the localized message from `views.dashboard.following_orgs.empty`.

### Admin viewing another user's followed organizations

1. An administrator navigates to the followed organizations dashboard page with a `username` query parameter specifying another user.
2. The controller resolves the target user by that username instead of the current session user.
3. The view renders the followed organizations belonging to the specified user, following the same card layout as the standard view.

### Page limit capped by per_page parameter

1. The user (or a client) provides a `per_page` query parameter when loading the page.
2. The controller's `follows_limit` helper clamps the value: if it exceeds `LIMIT_PER_PAGE_MAX` (1000), the maximum is used; otherwise the provided value is used; if absent, `LIMIT_PER_PAGE_DEFAULT` (80) applies.
3. The resulting follow collection is limited to the computed number of records.

## Design Intent

The page reuses the shared `following` dashboard layout pattern established for tags, users, and podcasts. The `fetch_and_authorize_user` helper centralizes the policy check and the admin-override logic for the target user, keeping the action itself concise. Pagination is done via a simple limit (rather than cursor or offset paging) to keep the implementation lightweight for a list that is unlikely to be extremely long.
