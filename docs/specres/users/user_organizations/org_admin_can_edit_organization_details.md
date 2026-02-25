---
id: "01KJ9N1ZPXHEHSP60VT4S49QQB"
name: "org_admin_can_edit_organization_details"
status: "in-development"
---

## Related Files

- `app/controllers/organizations_controller.rb`
- `app/views/users/_org_admin.html.erb` (Template)
- `spec/requests/user/user_organization_spec.rb` (Test)

## Functional Overview

An organization admin can edit their organization's profile details from the user-facing settings page. The edit form is located in the "Details" section of the org admin settings partial and allows the admin to update fields such as name, slug, profile image, social links (Twitter, GitHub, website URL), tag line, summary, location, email, company size, story, tech stack, and CTA (call-to-action) fields. On a valid submission the organization record is updated, all member caches are invalidated via a `touch_all` on `organization_info_updated_at`, a success flash notice is set, and the user is redirected to the organization settings page. If validation fails, the form is re-rendered with errors displayed.

## Design Intent

All string parameters submitted through the organization form are sanitized with `strip_tags` before persistence to prevent HTML injection. The `profile_updated_at` timestamp is merged into the update call so that dependent systems (e.g., feed caches) know the organization profile has changed. Touching `organization_info_updated_at` on all member users ensures that per-user caches reflecting organization data are invalidated in a single bulk operation rather than one-by-one.

## Key Members

- `ORGANIZATIONS_PERMITTED_PARAMS` — strong-parameters allowlist covering all editable profile fields: `name`, `slug`, `summary`, `tag_line`, `url`, `proof`, `profile_image`, `location`, `company_size`, `tech_stack`, `email`, `story`, `bg_color_hex`, `text_color_hex`, `twitter_username`, `github_username`, `cta_button_text`, `cta_button_url`, `cta_body_markdown`
- `organization_params` — private method that requires the `organization` key, permits the allowlist, and strips HTML tags from all string values
- `profile_updated_at` — merged into the update to mark the time of last profile edit
- `organization_info_updated_at` — touched on all member users after a successful update to invalidate member-level caches
- `valid_image?` — guard called before `update`; renders the edit template immediately if the uploaded profile image fails file-type or filename-length validation

## Scenarios

### Successful update of profile fields

1. An authenticated org admin submits the organization edit form with valid values for any combination of profile fields (name, slug, summary, tag line, social links, location, email, company size, story, tech stack, etc.)
2. The controller verifies the uploaded profile image passes file-type and filename-length checks (or no image was submitted)
3. The organization record is updated with the sanitized params and the current timestamp as `profile_updated_at`
4. All users who are members of the organization have their `organization_info_updated_at` column touched to bust downstream caches
5. A success flash notice is set and the admin is redirected to `/settings/organization`

### Validation failure on required or constrained fields

1. An authenticated org admin submits the organization edit form with invalid data (e.g., a slug that is already taken or violates format rules, or a name that exceeds 50 characters)
2. The `Organization#update` call returns false due to model-level validation errors
3. The controller reloads the membership list (`@org_organization_memberships`) and the current user's membership record (`@organization_membership`) to populate the form re-render
4. The edit template (`users/edit`) is re-rendered with the validation errors visible to the admin; no redirect occurs

### Invalid profile image upload

1. An authenticated org admin submits the organization edit form including a profile image attachment
2. The image fails either the file-type check (not a file object) or the filename-length check (original filename exceeds the allowed limit)
3. The controller adds the appropriate error to `@organization.errors[:profile_image]` and immediately re-renders the edit template without attempting to persist any changes

### Updating CTA fields

1. An authenticated org admin fills in the CTA section of the edit form: `cta_body_markdown` (up to 256 characters), `cta_button_text` (up to 20 characters), and `cta_button_url` (up to 150 characters)
2. The form is submitted and passes image validation
3. The organization record is updated with the new CTA values alongside any other submitted profile fields
4. A success flash notice is set and the admin is redirected to `/settings/organization`

## Failures / Exceptions

- If the submitted profile image is not a real file object, the update is aborted and the error "invalid file type" is added to the organization
- If the submitted profile image's filename exceeds the maximum allowed length, the update is aborted and the error "filename too long" is added to the organization
- If `Organization#update` fails for any model validation reason, the admin is shown the form again with errors rather than being redirected; no partial save occurs
- Non-admin organization members are not authorized to reach the update action; Pundit raises `NotAuthorizedError`
