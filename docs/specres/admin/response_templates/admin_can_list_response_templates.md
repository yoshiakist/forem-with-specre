---
id: "01KJ7H3CSDJE9JT7EXNH64N3TW"
name: "admin_can_list_response_templates"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/response_templates_controller.rb`
- `app/models/response_template.rb`
- `app/policies/response_template_policy.rb`
- `spec/requests/admin/response_templates_spec.rb` (Test)
- `app/views/admin/response_templates/index.html.erb` (Template)

## Functional Overview

Admin users (full admins and single-resource admins for ResponseTemplate) can access the response templates listing page at `GET /admin/advanced/response_templates`. The index action fetches all response templates, with optional filtering by `type_of` via a query parameter. Results are paginated at 50 records per page. The page displays each template's title, type, and associated username in a table, and provides a link to create a new template.

## Design Intent

The optional `filter` parameter allows admins to narrow the listing to templates of a specific `type_of` (e.g. `mod_comment`, `email_reply`) without requiring a separate endpoint. Access is restricted to any admin role via `admin_index?` in the policy, which delegates to `user_any_admin?`.

## Key Members

- `TYPE_OF_TYPES` — the allowed template type values: `personal_comment`, `mod_comment`, `abuse_report_email_reply`, `email_reply`, `tag_adjustment`
- `params[:filter]` — optional query parameter to narrow results to a single `type_of`
- `params[:page]` — page number for Kaminari pagination (50 records per page)

## Scenarios

### Admin views all response templates

1. An authenticated admin navigates to the response templates index page.
2. The system fetches all response templates from the database, paginated at 50 per page.
3. The page renders a table listing each template's title (as an edit link), type, and associated username (if any).
4. A "Create new template" button is shown at the top of the page.

### Admin filters response templates by type

1. An authenticated admin requests the index page with a `filter` query parameter set to a valid `type_of` value (e.g. `mod_comment`).
2. The system fetches only response templates whose `type_of` matches the filter value, then paginates the results.
3. The page renders only the matching templates in the table.

### Single-resource admin accesses the listing

1. A user with the single-resource admin role scoped to `ResponseTemplate` signs in and visits the index page.
2. The policy's `admin_index?` check passes because the user satisfies `user_any_admin?`.
3. The page renders with HTTP 200, identical to a full admin's view.
