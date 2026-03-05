---
id: "01KJ7H3X733B2JBXBQJVRQQZE8"
name: "admin_can_edit_response_template"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/response_templates_controller.rb`
- `app/models/response_template.rb`
- `app/policies/response_template_policy.rb`
- `spec/requests/admin/response_templates_spec.rb` (Test)
- `app/views/admin/response_templates/edit.html.erb` (Template)
- `app/views/admin/response_templates/_form.html.erb` (Template)

## Functional Overview

An admin or super moderator can edit an existing response template by navigating to its edit page, modifying any combination of its fields (type of template, title, content body, content type, and optionally a user identifier to restrict the template to a single user), and submitting the form. On a valid update the record is saved, a success flash message is shown, and the admin is redirected back to the same edit page. On a validation failure the edit form is re-rendered with an inline error message. Every mutating action (create, update, destroy) is recorded by the audit logger.

## Design Intent

The update action resolves permitted attributes through Pundit (`permitted_attributes(ResponseTemplate)`), which limits fields to `content_type`, `content`, and `title` for updates — preventing callers from changing ownership or template type after creation. The `modify?` policy method gates both update and destroy, allowing the record owner or an admin/super moderator acting on a `mod_comment` template to proceed.

## Key Members

- `type_of` — one of `personal_comment`, `mod_comment`, `abuse_report_email_reply`, `email_reply`, `tag_adjustment`
- `content_type` — one of `plain_text`, `html`, `body_markdown`; must match the type_of category (comments require `body_markdown`, emails require `plain_text` or `html`)
- `user_identifier` — virtual attribute resolved to a user by username, email, or ID; blank means the template is shared

## Scenarios

### Viewing the edit form with current values

1. An authenticated admin visits the edit path for an existing response template.
2. The controller finds the record by ID and assigns it to `@response_template`.
3. The edit view renders with the template's current title, content, content type, and type_of values pre-populated in the form fields.
4. A delete button is also rendered, protected by a browser confirmation dialog.

### Successful update

1. The admin modifies one or more fields in the form and submits it.
2. The controller resolves the `user_identifier` param to a user record (or nil if blank) and assigns it.
3. The record is updated using only the policy-permitted attributes (`content_type`, `content`, `title`).
4. A success flash message is set and the admin is redirected back to the same edit page.
5. The audit logger records the action with the current user and request params.

### Validation failure — content type mismatch

1. The admin submits an update that sets a content type incompatible with the template's type (e.g., `html` for a `mod_comment`).
2. The model validation rejects the change and adds an error message.
3. The controller sets a danger flash message with the formatted error sentence and re-renders the edit form.

### Validation failure — content uniqueness conflict

1. The admin updates the content to a value that already exists for the same combination of user, type_of, and content_type.
2. The uniqueness validation on `content` fails.
3. The controller re-renders the edit form with the error.

## Failures / Exceptions

- If the `type_of` field is set to a user-nil type (e.g., `mod_comment`) while a user is associated, the `user_nil_only_for_user_nil_types` validation adds an error and the update is rejected.
- The `errors_as_sentence` helper formats all model errors into a single string for the flash danger message.
