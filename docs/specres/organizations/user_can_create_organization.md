---
id: "01KJ028T8Z2686ZJZX4WNS2VTQ"
name: "user_can_create_organization"
status: "draft"
---

## Related Files

- `app/controllers/organizations_controller.rb`
- `app/models/organization.rb`
- `app/models/organization_membership.rb`
- `app/policies/organization_policy.rb`

## Functional Overview

An authenticated user who is not spam or suspended can submit a form to create a new organization. The system validates the submitted profile image (if any), builds an `Organization` record from the permitted parameters, authorizes the action via `OrganizationPolicy#create?`, and saves it. On success, the creating user is automatically enrolled as an `admin`-level `OrganizationMembership`, a rate-limit counter is incremented, a success flash message is set, and the user is redirected to the organization's settings page. If the image is invalid, or if model validation fails, the form is re-rendered with errors so the user can correct them.

## Key Members

- `ORGANIZATIONS_PERMITTED_PARAMS` — exhaustive allowlist of scalar fields accepted from the form (name, summary, slug, url, profile_image, etc.)
- `type_of_user: "admin"` — the role assigned to the creator's `OrganizationMembership`
- `OrganizationPolicy#create?` — permits any user who is not spam or suspended

## Scenarios

### Successful creation

1. An authenticated, non-suspended user navigates to the new-organization form and submits it with a valid name, slug, profile image, and any optional fields.
2. The system validates the submitted image: it must be a file object and the filename must not exceed the length limit.
3. The system builds an `Organization` from the permitted params, stripping all HTML tags from string values, and authorizes the action.
4. The record passes all model validations (name and profile image present, slug unique across models, field lengths within bounds, valid hex colors, valid URLs, etc.) and is saved.
5. A 100-character secret is auto-generated before save. Cache-busting and social-image generation are enqueued after save.
6. An `OrganizationMembership` is created linking the current user to the new organization with `type_of_user: "admin"`.
7. The organization-creation rate-limit counter is incremented for the current user.
8. A success flash notice is set and the user is redirected to `/settings/organization/<id>`.

### Invalid profile image

1. The user submits the form with an attached file that is not a valid image or has an excessively long filename.
2. The image validation fails before any `Organization` record is built; an error is added to `@organization.errors[:profile_image]`.
3. The `users/edit` template is re-rendered so the user can correct the image.

### Model validation failure

1. The user submits the form with a missing or invalid field (e.g., name absent, slug already taken, URL in wrong format, color value not a valid hex string).
2. The `Organization` record fails to save; model validation errors are collected.
3. The `users/edit` template is re-rendered with the validation errors displayed.

### Unauthorized user (spam or suspended)

1. A user whose account is flagged as spam or suspended submits the creation form.
2. `OrganizationPolicy#create?` returns false, and Pundit raises an authorization error.
3. The request is blocked; no organization or membership record is created.

## Failures / Exceptions

- If the attached profile image is not a file object, `profile_image is_not_file_message` error is added and the form is re-rendered without saving.
- If the profile image filename is too long, `profile_image filename_too_long_message` error is added and the form is re-rendered.
- If `Organization#save` returns false due to validation errors, the form is re-rendered with errors; no membership is created.
- `OrganizationMembership.create!` is called (bang form), so any unexpected failure there would raise `ActiveRecord::RecordInvalid` and bubble up as an unhandled exception.
