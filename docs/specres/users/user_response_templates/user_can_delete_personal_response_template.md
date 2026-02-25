---
id: "01KJ9KKBB0PGJK2Y32KDWSYK1K"
name: "user_can_delete_personal_response_template"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/response_templates_controller.rb`
- `app/models/response_template.rb`
- `app/policies/response_template_policy.rb`
- `spec/requests/response_templates_spec.rb` (Test)
- `spec/policies/response_template_policy_spec.rb` (Test)

## Functional Overview

A signed-in user can permanently delete a personal response template that they own. The controller's `destroy` action looks up the template by its ID parameter, authorizes the request via `ResponseTemplatePolicy`, and calls `destroy` on the record. On success, a localized notice is set in the flash and the user is redirected to the response-templates tab of their settings page. If destruction fails, the model's validation errors are shown via a flash error instead.

## Scenarios

### Successful deletion

1. The signed-in user sends a DELETE request to `/response_templates/:id` where the template belongs to them.
2. The system authorizes the action; `ResponseTemplatePolicy#destroy?` returns `true` because the requesting user is the record's owner.
3. The template is permanently removed from the database.
4. A success notice is stored in the flash and the user is redirected to the response-templates settings tab.

### Unauthorized deletion attempt (non-owner)

1. A signed-in user sends a DELETE request for a template that belongs to a different user.
2. `ResponseTemplatePolicy#destroy?` returns `false` because the requesting user is not the record's owner and the template is not a `mod_comment`.
3. Pundit raises `Pundit::NotAuthorizedError`; the request is not processed further.

### Unauthenticated deletion attempt

1. A request arrives without a valid session (no signed-in user).
2. Pundit raises `Pundit::NotAuthorizedError` before any database access occurs.

## Failures / Exceptions

- **Authorization failure:** Any attempt to delete a template not owned by the current user raises `Pundit::NotAuthorizedError` (via Pundit's `after_action :verify_authorized` guard).
- **Destroy failure:** If `ActiveRecord#destroy` returns false (e.g., due to a before-destroy callback), the model's validation errors are written to `flash[:error]` and the user is still redirected to the settings page without the record being removed.
