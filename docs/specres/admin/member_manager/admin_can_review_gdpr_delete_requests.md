---
id: "01KJBEERZREF0ZGB6E62EATBXE"
name: "admin_can_review_gdpr_delete_requests"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/admin/gdpr_delete_requests_controller.rb`
- `app/models/gdpr_delete_request.rb`
- `app/queries/admin/gdpr_delete_requests_query.rb`
- `app/views/admin/gdpr_delete_requests/index.html.erb` (Template)
- `spec/queries/admin/gdpr_delete_requests_query_spec.rb` (Test)
- `spec/requests/admin/gdpr_delete_requests_spec.rb` (Test)

## Functional Overview

Admins can view and manage outstanding GDPR account deletion requests through a paginated, searchable admin interface. The index page lists all pending requests with their associated username, email, and submission date, and supports full-text search against both the email and username fields. When an admin confirms a request by clicking the "Deleted" button, the record is removed from the database and an audit log entry is created to preserve a record of who performed the deletion and for which user. If confirmation fails for any reason, a danger flash message is shown and the admin is redirected back to the list.

## Design Intent

The query layer is separated into `Admin::GDPRDeleteRequestsQuery` to keep the controller thin and make search logic independently testable. The search uses a case-insensitive `ILIKE` clause across both email and username columns so admins can locate a request regardless of which field they remember. Audit logging is performed synchronously immediately after destruction so that every confirmed deletion is traceable to a specific admin identity and timestamp.

## Key Members

- `search` (string, optional) — partial match applied against email and username via `ILIKE`; empty or absent means return all records
- `page` / `per(50)` — Kaminari-based pagination, 50 records per page
- `AuditLog` category `"admin.gdpr_delete.confirm"` — the event written on successful confirmation; records acting admin and target `user_id`

## Scenarios

### Admin views the list of GDPR delete requests

1. An authenticated super-admin navigates to the GDPR delete requests admin page.
2. The system retrieves all pending requests ordered by creation date (newest first) and paginates them at 50 per page.
3. The page renders each request's username, email, submission date, and a "Deleted" confirmation button.
4. A count badge displays the total number of outstanding requests; the badge is omitted when the list is empty.

### Admin searches for a specific request

1. The admin types a partial or full email address or username into the search field and submits.
2. The system filters requests using a case-insensitive partial match against both the email and username columns.
3. Only matching records are returned; if no records match, an empty state message is shown.

### Admin confirms a GDPR deletion request

1. The admin clicks the "Deleted" button for a specific request; a confirmation modal is displayed.
2. The admin confirms the action.
3. The system destroys the `GDPRDeleteRequest` record and writes an `AuditLog` entry recording the acting admin's identity and the target user's ID.
4. A success flash message is shown and the admin is redirected to the updated list.

### Admin encounters an error during confirmation

1. The admin confirms deletion of a request.
2. An unexpected error occurs during destruction (e.g., a database constraint violation).
3. The system catches the error, displays a danger flash message containing the error details, and redirects the admin back to the list without deleting the record or writing an audit log.

## Failures / Exceptions

- If `GDPRDeleteRequest#destroy` raises a `StandardError`, the exception message is surfaced as a flash danger alert and no audit log is written.
- A `GDPRDeleteRequest` that cannot be found by ID will raise `ActiveRecord::RecordNotFound` (unhandled; results in a 404 from the framework).
