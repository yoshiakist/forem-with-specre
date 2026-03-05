---
id: "01KJ7H6DWTE1GHSKNKFFQC1NC9"
name: "admin_can_delete_response_template"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/response_templates_controller.rb`
- `app/models/response_template.rb`
- `app/policies/response_template_policy.rb`
- `app/views/admin/response_templates/edit.html.erb` (Template)
- `spec/requests/admin/response_templates_spec.rb` (Test)

## Functional Overview

An admin can permanently delete a response template through the admin panel. The delete action is triggered from the edit page via a form submission with a browser confirmation dialog. The controller finds the template by ID, destroys it, sets a flash success message, and redirects back to the referring page (falling back to the response templates index). Every destructive action is automatically audit-logged through an `after_action` callback that records the moderator's activity. Authorization is enforced via `ResponseTemplatePolicy#destroy?`, which is aliased to `modify?` and permits the record's owner or an admin/super_moderator acting on a `mod_comment`-type template.

## Scenarios

### Successful deletion with browser confirmation

1. The admin navigates to the edit page for a response template.
2. The edit page renders a "Delete" button inside a form that submits a DELETE request; the form's `onsubmit` handler shows a browser confirmation dialog asking "Are you sure you want to delete this response template?".
3. The admin confirms the dialog.
4. The controller finds the template by ID, calls destroy on it, and sets a success flash message containing the deleted template's title.
5. The admin is redirected back to the referring page (or to the response templates index if no referrer is available).

### Audit log recorded after deletion

1. After the destroy action completes (whether successful or not), the `after_action` callback fires.
2. `Audit::Logger.log` is called with the `:moderator` category, the current user, and the request parameters, creating a permanent audit trail of the deletion.

### Authorization enforcement

1. When a DELETE request arrives, Pundit evaluates `ResponseTemplatePolicy#destroy?` (aliased to `modify?`).
2. The policy allows deletion if the requester is the record's owner, or if the template is of type `mod_comment` and the requester is an admin or super_moderator.
3. Requests that do not satisfy either condition are rejected before the destroy action executes.

## Failures / Exceptions

- If `destroy` fails (unlikely given the comment in the code), the controller sets a danger flash with the model's validation errors as a sentence and still redirects back rather than re-rendering a form.
