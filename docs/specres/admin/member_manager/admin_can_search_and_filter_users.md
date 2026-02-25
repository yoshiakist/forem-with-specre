---
id: "01KJ9MXNY671JQVR29GGYXMVQF"
name: "admin_can_search_and_filter_users"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `app/queries/admin/users_query.rb`
- `app/helpers/admin/users_helper.rb`
- `spec/queries/admin/users_query_spec.rb` (Test)
- `spec/helpers/admin/users_helper_spec.rb` (Test)
- `spec/requests/admin/users_spec.rb` (Test)
- `app/views/admin/users/index.html.erb` (Template)
- `app/views/admin/users/index/_applied_filters.html.erb` (Template)
- `app/views/admin/users/index/_controls.html.erb` (Template)
- `app/views/admin/users/index/_filters_modal.html.erb` (Template)
- `app/views/admin/users/index/_invitation_actions_dropdown.html.erb` (Template)
- `app/views/admin/users/index/_member_data.html.erb` (Template)
- `app/views/admin/users/index/_member_image.html.erb` (Template)
- `app/views/admin/users/index/_status_indicator.html.erb` (Template)
- `app/views/admin/users/index/_user_actions_dropdown.html.erb` (Template)
- `app/views/admin/users/index/_user_status_indicator.html.erb` (Template)
- `app/views/admin/users/controls/_expand_search_button.html.erb` (Template)
- `app/views/admin/users/controls/_search_field.html.erb` (Template)
- `app/javascript/packs/admin/users/memberIndex.js`
- `app/javascript/packs/admin/users/filtersModal.js`
- `app/javascript/packs/admin/users/controls.js`
- `app/javascript/packs/admin/convertUserIdsToUsernameInputs.js`

## Functional Overview

An admin can visit the user index page to list all registered users, search them by name, email, or username, and apply filters by role, status, organization membership, and registration date range. The `index` action responds to both HTML (paginated, up to 50 per page) and JSON (used for inline lookups, returning only id, name, and username). All filtering logic is delegated to `Admin::UsersQuery`. The `Admin::UsersHelper` provides display helpers for rendering role labels, status indicators, organization tooltips, and color-coded status badges throughout the index UI.

## Key Members

- `search: String` — case-insensitive substring matched against `users.name`, `users.email`, and `users.username` via `ILIKE`
- `role: String` — legacy single-role filter; maps directly to a Rolify `with_role` scope (e.g. `"super_admin"`, `"tag_moderator"`)
- `roles: Array<String>` — multi-role filter using label strings from `Constants::Role::ALL_ROLES_LABELS_TO_WHERE_CLAUSE` (e.g. `["Admin", "Tech Admin"]`); takes precedence over `role` when present
- `statuses: Array<String>` — subset of base-role labels (e.g. `["Warned", "Comment Suspended"]`); merged with `roles` when both are given
- `organizations: Array<Integer>` — list of organization IDs; restricts results to users who are members of any of those organizations
- `joining_start: String` — lower bound for `registered_at`, parsed according to `date_format`
- `joining_end: String` — upper bound for `registered_at`, parsed according to `date_format`
- `date_format: String` — UI date format for parsing joining bounds; `"DD/MM/YYYY"` (default) or `"MM/DD/YYYY"`
- `ids: Array<Integer>` — explicit list of user IDs; used by the JSON endpoint for typeahead lookups
- `limit: Integer` — cap on result count; ignored when zero, nil, or non-numeric; used by the JSON endpoint

## Scenarios

### Admin lists all users without filters

1. An authenticated admin navigates to the admin users index page (`GET /admin/member_manager/users`).
2. The controller calls `Admin::UsersQuery` with no filter parameters against the `User.registered` relation.
3. All registered users are returned, ordered by `created_at` descending, paginated at 50 per page.
4. The page renders each user's name, username, status indicator, role badge, and organization memberships.

### Admin searches users by name, email, or username

1. The admin types a search term into the search field on the index page.
2. The controller passes the `search` parameter to `Admin::UsersQuery`.
3. The query applies a case-insensitive `ILIKE` match against `name`, `email`, and `username` simultaneously.
4. Only users whose name, email, or username contains the search substring are returned, still ordered by `created_at` descending.

### Admin filters users by role and/or status

1. The admin opens the filters modal and selects one or more roles (e.g. "Admin", "Super Admin") and/or statuses (e.g. "Warned", "Comment Suspended").
2. The controller passes `roles` and `statuses` to `Admin::UsersQuery`; the two arrays are merged before filtering.
3. The query builds a subquery over the `roles` table, matching each label to its corresponding role name and optional resource type, and restricts users to those present in the subquery.
4. The index page re-renders showing only users that hold at least one of the selected roles or statuses, and the applied-filters partial displays the active filter chips.

### Admin filters users by organization and join date range

1. The admin selects one or more organizations and sets a joining start and/or end date in the filters modal.
2. The controller passes `organizations`, `joining_start`, `joining_end`, and `date_format` to `Admin::UsersQuery`.
3. The query restricts the result set to users who have an `OrganizationMembership` record for any of the selected organizations, and whose `registered_at` falls within the supplied date bounds (start is inclusive from beginning-of-day; end is inclusive through end-of-day).
4. Multiple active filters are combined with AND logic, so only users matching all criteria are returned.

### Inline JSON lookup by IDs or search term

1. A JavaScript component (e.g. a user-ID-to-username converter) issues a `GET /admin/member_manager/users.json` request with `ids` or `search` and an optional `limit` parameter.
2. The controller detects the JSON format and calls `Admin::UsersQuery` with only `search`, `ids`, and `limit`.
3. The query returns matching users capped by `limit` (when positive), ordered by `created_at` descending.
4. The controller renders a JSON array containing only `id`, `name`, and `username` for each matched user.

## Failures / Exceptions

- When `joining_start` or `joining_end` cannot be parsed for the given `date_format`, `DateTime.strptime` raises an `ArgumentError`; no rescue is defined in the query, so the error propagates to the controller's default error handling.
- When the `role` parameter is provided but does not correspond to a recognized Rolify role, `with_role` returns an empty relation silently.
- When `roles` contains a label not present in `Constants::Role::ALL_ROLES_LABELS_TO_WHERE_CLAUSE`, `Hash#fetch` raises a `KeyError`.
- The `limit` parameter is silently ignored when its value is zero, nil, or a non-numeric string; no error is raised and all matching users are returned.
- "Good Standing" is intentionally excluded from the filterable statuses list because it does not map to a discrete role; attempting to filter by it via the `roles`/`statuses` arrays would raise a `KeyError`.
