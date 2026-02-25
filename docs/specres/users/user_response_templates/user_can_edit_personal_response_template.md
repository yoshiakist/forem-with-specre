---
id: "01KJ9KH5SRKY1NSYR3C4JH0TM2"
name: "user_can_edit_personal_response_template"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/response_templates_controller.rb`
- `app/models/response_template.rb`
- `app/policies/response_template_policy.rb`
- `app/views/users/_response_template.html.erb` (Template)
- `app/views/users/_response_templates.html.erb` (Template)
- `spec/requests/response_templates_spec.rb` (Test)
- `spec/policies/response_template_policy_spec.rb` (Test)

## Functional Overview

A signed-in user can update the title and content of a personal response template they own. The `ResponseTemplatesController#update` action loads the template by ID, authorizes the request via `ResponseTemplatePolicy`, and applies the permitted attributes (`content_type`, `content`, `title`). On success, the user is redirected to the response-templates settings page with a confirmation notice. On validation failure, the user is redirected back to the edit form with the previously submitted title and content preserved as query parameters so the form can repopulate without data loss. Users who do not own the template and are not authorized moderators are denied with `Pundit::NotAuthorizedError`.

## Scenarios

### Successful edit

1. A signed-in user navigates to the edit form for a response template they own.
2. The user changes the title or content and submits the form.
3. The controller loads the template by its ID and confirms the current user is the owner via `ResponseTemplatePolicy#update?`.
4. The template is updated with the permitted attributes.
5. The user is redirected to the response-templates settings tab with a success flash notice and the template's ID in the URL.

### Validation failure (blank title)

1. A signed-in user submits the edit form with a blank title.
2. The controller attempts to update the template but the model validation fails.
3. The user is redirected back to the edit form.
4. The previously submitted title and content are included as query parameters so the form can restore the unsaved input.

### Unauthorized edit attempt (not the owner)

1. A signed-in user submits a PATCH request to update a personal response template they do not own.
2. `ResponseTemplatePolicy#update?` evaluates that the user is neither the owner nor an authorized moderator acting on a `mod_comment` template.
3. The request is denied with `Pundit::NotAuthorizedError`.

### Unauthorized edit attempt (trusted user on mod_comment)

1. A trusted (but non-moderator) user submits a PATCH request targeting a `mod_comment` template.
2. `ResponseTemplatePolicy#update?` determines the user is neither the owner nor an admin or super-moderator.
3. The request is denied with `Pundit::NotAuthorizedError`.

## Failures / Exceptions

- **Validation error**: If the model is invalid (e.g., blank title), the controller redirects back to the edit form with `previous_title` and `previous_content` query parameters carrying the submitted values.
- **Not authorized**: If Pundit denies the action, `Pundit::NotAuthorizedError` is raised; the `ApplicationController` rescue handler converts this to an appropriate error response.
- **Record not found**: If the ID in the URL does not correspond to an existing template, `ActiveRecord::RecordNotFound` is raised.
