---
id: "01KJ9MT3FSYT9TTRKCNCH9Q9GV"
name: "admin_can_build_custom_user_queries"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/user_queries_controller.rb`
- `app/models/user_query.rb`
- `app/services/user_query_executor.rb`
- `app/services/user_query_validator.rb`
- `app/services/user_query_variable_substitutor.rb`
- `spec/controllers/admin/user_queries_controller_spec.rb` (Test)
- `spec/models/user_query_spec.rb` (Test)
- `spec/services/user_query_executor_spec.rb` (Test)
- `spec/services/user_query_validator_spec.rb` (Test)
- `spec/factories/user_queries.rb` (Test)
- `app/views/admin/user_queries/index.html.erb` (Template)
- `app/views/admin/user_queries/show.html.erb` (Template)
- `app/views/admin/user_queries/new.html.erb` (Template)
- `app/views/admin/user_queries/edit.html.erb` (Template)

## Functional Overview

Super admins can create, edit, and delete named SQL queries that target the users table. Each query has an optional description, variable definitions in JSON format, and a configurable execution time limit. The index page supports filtering by active status and free-text search across name and description. A test-execute action runs the query against a limited sample of users so admins can verify correctness before activating it. A toggle-active action enables or disables individual queries. A validate endpoint accepts a raw SQL string and returns a JSON response indicating whether the query is structurally acceptable, powering real-time feedback in the form UI.

## Design Intent

Queries are kept read-only by design — the validator rejects any statement that is not a plain SELECT targeting the users table. This prevents accidental data modification through the admin UI. Variable interpolation using `{{variable_name}}` placeholders allows queries to be reused across different execution contexts without editing the stored SQL. The test-execute action is intentionally separate from full execution and operates with a caller-supplied limit, making it safe to preview results without touching all matching users.

## Key Members

- `name` — human-readable label for the query, required and unique
- `description` — optional free text explaining what segment the query targets
- `query` — the raw SQL string; must be a read-only SELECT against the users table; max 10,000 characters
- `variable_definitions` — JSON object whose keys map to `{{placeholder}}` tokens in the query SQL
- `max_execution_time_ms` — timeout for full execution, between 1,000 and 300,000 ms
- `active` — boolean flag; only active queries may be executed
- `created_by` — reference to the admin user who created the record, set automatically on create

## Scenarios

### Admin lists and filters user queries

1. Admin navigates to the user queries index.
2. The system loads all queries ordered by creation date, paginated at 20 per page, with creator names eagerly loaded.
3. Admin optionally enters a search term; the system filters to queries whose name or description contains the term (case-insensitive).
4. Admin optionally selects an active/inactive filter; the system narrows results to that status.
5. The filtered, paginated list is rendered.

### Admin creates a new user query

1. Admin opens the new query form and fills in name, description, SQL, variable definitions, execution timeout, and active flag.
2. The form provides real-time inline validation by calling the validate endpoint as the admin types into the SQL field.
3. On submit, the system saves the record and sets `created_by` to the current admin.
4. On success the admin is redirected to the query detail page with a success notice.
5. On validation failure the form is re-rendered with error messages and an HTTP 422 status.

### Admin edits an existing user query

1. Admin opens the edit form for an existing query.
2. Admin modifies any permitted field (name, description, SQL, variable definitions, timeout, active flag).
3. On submit, the system updates the record.
4. On success the admin is redirected to the detail page with a success notice.
5. On validation failure the edit form is re-rendered with error messages and an HTTP 422 status.

### Admin test-executes a query

1. From the query detail page, admin submits the test-execute form with an optional limit (default 10, max 100).
2. The system delegates to `UserQueryExecutor` with the given limit.
3. If execution succeeds, the matched users are displayed in the detail view alongside a success flash message showing the count.
4. If `UserQueryExecutor` reports errors, an alert flash is shown and the error list is rendered in the view.
5. If an unexpected exception is raised, it is caught, its message stored in `@execution_errors`, and an alert flash is displayed.

### Admin toggles a query's active status

1. Admin clicks the activate or deactivate button on either the list or detail page.
2. The system flips the `active` flag unconditionally.
3. The admin is redirected to the detail page with a notice indicating whether the query was activated or deactivated.

### Admin validates a SQL query via JSON endpoint

1. The form (new or edit) calls the validate endpoint with a raw SQL string as the admin types.
2. The system passes the string to `UserQueryValidator` and responds with JSON containing `valid` (boolean) and `errors` (array of strings).
3. Valid queries display a green confirmation in the form; invalid queries display the error list in red.

## Failures / Exceptions

- Creating or updating with an empty name, a non-SELECT query, or other model validation failures causes a 422 response and re-renders the form with inline error messages.
- A runtime exception during test execution is rescued at the controller level; the message is surfaced as an alert flash and the detail view is re-rendered rather than returning a 500 error.
- Non-admin users attempting to access any action receive `Pundit::NotAuthorizedError` from the inherited `Admin::ApplicationController` authorization layer.
