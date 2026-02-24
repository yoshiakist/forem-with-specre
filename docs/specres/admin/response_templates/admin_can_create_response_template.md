---
id: "01KJ7H3RYFNKHXHYQZYPD2PCYC"
name: "admin_can_create_response_template"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/response_templates_controller.rb`
- `app/models/response_template.rb`
- `app/policies/response_template_policy.rb`
- `spec/requests/admin/response_templates_spec.rb` (Test)
- `app/views/admin/response_templates/new.html.erb` (Template)
- `app/views/admin/response_templates/_form.html.erb` (Template)

## Functional Overview

An admin or super-moderator can create a new response template via the admin panel. The creation form collects a type (`type_of`), title, body content, content type, and an optional user identifier that restricts the template to a single user. On submission, the controller resolves the user identifier to a User record via `UsersQuery`, validates the template against model rules (required fields, valid `type_of` and `content_type` enum values, content-type compatibility with template type, per-user template count limits), saves the record, and redirects to the index with a success flash. If validation fails, errors are displayed and the form is re-rendered. Every create action is recorded in the audit log regardless of outcome.

## Key Members

- `TYPE_OF_TYPES` — allowed values: `personal_comment`, `mod_comment`, `abuse_report_email_reply`, `email_reply`, `tag_adjustment`
- `USER_NIL_TYPE_OF_TYPES` — types that must not have an associated user: `mod_comment`, `abuse_report_email_reply`, `email_reply`, `tag_adjustment`
- `CONTENT_TYPES` — allowed values: `plain_text`, `html`, `body_markdown`
- `user_identifier` — virtual attribute; resolved to a User by username, email, or ID before save

## Scenarios

### Successful creation

1. An admin navigates to `GET /admin/advanced/response_templates/new`, which renders the creation form.
2. The admin fills in type, title, content, content type, and optionally a user identifier, then submits the form.
3. The controller resolves the user identifier to a User record (or leaves `user` nil if the field is blank).
4. The template passes all model validations and is saved to the database.
5. A success flash message is set and the admin is redirected to the response templates index.

### User identifier lookup

1. The admin enters a username, email address, or numeric ID in the user identifier field.
2. On form submission, the controller passes the identifier to `UsersQuery.find`.
3. The resolved User is assigned to the template before saving; the template is then scoped to that user.
4. If the identifier is blank, no user is assigned and the template is treated as a global (non-personal) template.

### Validation failure — content type incompatible with template type

1. The admin submits the form with a `type_of` value that includes "comment" (e.g., `mod_comment`) but selects a non-Markdown `content_type` such as `html`.
2. The model validation rejects the record because comment-type templates require `body_markdown`.
3. The controller sets a danger flash containing the validation error sentence and re-renders the new form.
4. The admin corrects the content type and resubmits.

### Validation failure — required field missing

1. The admin submits the form with a blank title, content, or other required field.
2. Model presence validations fail and return error messages.
3. The controller re-renders the new form with an error flash; the template is not saved.

### Audit logging

1. After any `create` action completes (success or failure at the controller level), the `after_action` callback fires.
2. `Audit::Logger.log(:moderator, current_user, params)` records the action, the acting admin, and the submitted parameters for audit trail purposes.

## Failures / Exceptions

- If a user is assigned but the `type_of` belongs to `USER_NIL_TYPE_OF_TYPES`, the model adds a validation error to `type_of` and rejects the record.
- If a user is assigned and is neither trusted nor has fewer than 30 existing templates, the model adds a validation error to `user` indicating the template limit has been reached.
- If content is not unique within the same `(user_id, type_of, content_type)` scope, a uniqueness validation error is raised.
