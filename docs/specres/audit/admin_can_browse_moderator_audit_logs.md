---
id: "01KJ6H94SE5S0ANVZZNR3NCZNG"
name: "admin_can_browse_moderator_audit_logs"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/moderator_actions_controller.rb`
- `app/views/admin/moderator_actions/index.html.erb` (Template)
- `spec/requests/admin/moderator_actions_spec.rb` (Test)

## Functional Overview

Admins and single-resource admins can browse a paginated, searchable list of moderator audit log entries. The index page retrieves `AuditLog` records filtered to the `MODERATOR_AUDIT_LOG_CATEGORY` category, ordered newest first, and paginates them at 25 per page. A search form allows filtering by the associated user's username using Ransack. Each row in the results table shows the log entry ID, linked username, a humanized description of the action and controller, the raw data payload, and the timestamp. Rows where no user is associated are displayed without a username link.

## Design Intent

The controller delegates filtering and ordering to Ransack, which keeps query construction declarative and allows the search form to map directly to Ransack predicates. Pagination is applied after ransacking so that search results are also paginated consistently.

## Key Members

- `@q` — Ransack search object scoped to `AuditLog` records of the moderator audit log category, used by both the search form and the result query
- `@moderator_actions` — Paginated result set (25 per page) derived from `@q`
- `AuditLog::MODERATOR_AUDIT_LOG_CATEGORY` — Constant that identifies which audit log category is displayed on this page

## Scenarios

### Admin views the moderator audit log index

1. An authenticated admin navigates to the moderator actions admin page
2. The system loads all audit log entries belonging to the moderator audit log category, ordered by creation date descending
3. The page renders a table showing each entry's ID, the username of the associated user (linked to their admin user page), a humanized description of the action, the raw data, and the timestamp
4. Results are paginated with 25 entries per page and pagination controls appear above and below the table

### Admin searches for audit logs by username

1. An authenticated admin submits the search form with a partial or full username
2. The system filters the audit log entries to those whose associated user's username contains the search term
3. The page re-renders the table showing only matching entries, still paginated

### Audit log entry has no associated user

1. An audit log entry exists in the moderator audit log category with no user attached
2. When an admin views the index, the row for that entry displays the ID, action description, data, and timestamp, but the user cell is empty (no link rendered)

### Non-admin is blocked from accessing the page

1. A user without admin privileges attempts to access the moderator actions admin page
2. The system raises a `Pundit::NotAuthorizedError`, blocking access to the page

### Single-resource admin can access the page

1. A user granted single-resource admin access specifically for `ModeratorAction` navigates to the moderator actions admin page
2. The system allows the request and renders the page successfully
