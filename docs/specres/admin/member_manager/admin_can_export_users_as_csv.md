---
id: "01KJ9N640BTKZ039JDADKS1S6Z"
name: "admin_can_export_users_as_csv"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `app/views/admin/users/export.csv.erb`
- `app/views/admin/users/controls/_export.html.erb`
- `spec/requests/admin/users/users_export_spec.rb` (Test)

## Functional Overview

An authenticated admin can trigger a CSV download of all registered users. The export action queries `User.registered`, selecting a fixed set of identity fields (`id`, `name`, `username`, `email`, `registered_at`) and activity timestamp fields (`registered`, `last_comment_at`, `last_article_at`, `latest_article_updated_at`, `last_reacted_at`, `profile_updated_at`, `last_moderation_notification`, `last_notification_activity`). Each user's associated organizations are eager-loaded. The response is delivered as a file attachment named `users.csv` with the `text/csv` content type. The CSV rows include a derived `last_activity` value and a list of organization names per user.

## Design Intent

Selecting only the required attributes via `ATTRIBUTES_FOR_CSV` and `ATTRIBUTES_FOR_LAST_ACTIVITY` constants limits the database payload and makes the exported column set explicit and stable. Eager-loading organizations with `.includes(:organizations)` prevents N+1 queries when the template serializes organization names per row.

## Key Members

- `ATTRIBUTES_FOR_CSV`: `[id, name, username, email, registered_at]` — identity fields included in every row
- `ATTRIBUTES_FOR_LAST_ACTIVITY`: `[registered, last_comment_at, last_article_at, latest_article_updated_at, last_reacted_at, profile_updated_at, last_moderation_notification, last_notification_activity]` — timestamp fields used to derive the most recent activity date
- `User.registered` — scope that excludes unregistered / soft-deleted accounts
- CSV columns (in order): Name, Username, Email address, Status, Joining date, Last activity, Organizations

## Scenarios

### Successful CSV download with user data

1. An admin visits the user admin index page and triggers the CSV export (e.g., via the export button in the controls partial).
2. The browser sends a GET request to the export endpoint with the `.csv` format.
3. The controller queries all registered users, selecting the identity and activity attributes, and eager-loads their organizations.
4. The response is returned with `Content-Type: text/csv` and `Content-Disposition: attachment; filename=users.csv`.
5. The CSV file is downloaded; the first line contains the headers: Name, Username, Email address, Status, Joining date, Last activity, Organizations.
6. Each subsequent line contains one row per registered user with values for all seven columns.

### CSV includes activity timestamps

1. The export is triggered for a set of users who have varying activity histories (comments, articles, reactions, profile updates, etc.).
2. For each user, the system inspects all activity timestamp fields from `ATTRIBUTES_FOR_LAST_ACTIVITY` and derives a single `last_activity` value representing the most recent recorded activity.
3. The derived `last_activity` date is formatted and written into the "Last activity" column of that user's CSV row.
4. If no activity timestamp is present, the column is left blank for that user.
5. The "Joining date" column reflects `registered_at`, formatted identically.
