---
id: "01KJ9KDY750N4VSKV6CZCMR4FS"
name: "user_can_create_personal_response_template"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/response_templates_controller.rb`
- `app/models/response_template.rb`
- `app/policies/response_template_policy.rb`
- `spec/requests/response_templates_spec.rb` (Test)
- `spec/models/response_template_spec.rb` (Test)
- `spec/policies/response_template_policy_spec.rb` (Test)
- `spec/factories/response_templates.rb` (Test)
- `app/views/users/_response_template.html.erb` (Template)
- `app/views/users/_response_templates.html.erb` (Template)

## Functional Overview

An authenticated user can submit a form to create a personal response template saved under their account. The controller enforces that non-moderator users always produce a `personal_comment` template with `body_markdown` as the content type, regardless of what the submitted parameters request. On success the user is redirected to the response-templates settings tab with the new template pre-selected. On validation failure the user is redirected back to the same tab with the previously entered title and content preserved in query parameters so the form can be pre-populated.

## Design Intent

Non-moderator users are never trusted to set `type_of` or `content_type` themselves. The controller unconditionally overwrites those fields to `personal_comment` and `body_markdown` before saving. This prevents privilege escalation where a regular user could attempt to inject a `mod_comment` template by crafting a raw POST request. The permitted attributes exposed by the policy also exclude `type_of` for non-moderators, providing a second layer of enforcement at the parameter-filtering level.

## Scenarios

### Successful creation

1. An authenticated user submits a POST request to `/response_templates` with a title and content.
2. The controller assigns the current user's ID, forces `type_of` to `personal_comment`, and forces `content_type` to `body_markdown`.
3. The record passes validation and is persisted.
4. The user is redirected to their settings page at the response-templates tab, with the new template's ID in the URL.

### Non-moderator attempts to create a mod_comment template

1. An authenticated regular user submits a POST request including `type_of: "mod_comment"` in the parameters.
2. Because the user lacks moderator access, the controller ignores the submitted type and overrides it to `personal_comment`.
3. The record is saved as a `personal_comment` template under the user's account.

### Validation failure (blank title)

1. A user submits a POST request with a missing or blank title.
2. The model's presence validation fails.
3. The controller redirects the user back to the response-templates settings tab, passing the previously entered title and content as query parameters so the form retains the user's input.

### Template count limit reached (non-trusted user)

1. A non-trusted user already has 30 personal response templates.
2. The user attempts to create one more template.
3. The model's `template_count` validation fails with an error indicating the per-user limit of 30 has been reached.
4. The controller redirects the user back to the settings tab with a flash error message and the previously entered content preserved.

### Trusted user is not subject to the template limit

1. A trusted user already has 30 or more personal response templates.
2. The user submits a new template.
3. The `template_count` validation is skipped for trusted users, so the record is saved successfully.

## Failures / Exceptions

- **Presence validation:** `type_of`, `content_type`, `content`, and `title` must all be present; any missing field causes a validation error and a redirect with preserved form input.
- **Content type restriction for comment templates:** If `type_of` includes the word `"comment"`, the `content_type` must be `body_markdown`; any other value (e.g., `html`) is rejected.
- **Uniqueness constraint:** A user cannot create two templates with the same combination of `content`, `type_of`, and `content_type`.
- **Per-user limit:** Non-trusted users are limited to 30 templates. Exceeding this limit produces a validation error on the `user` attribute.
