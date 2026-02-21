---
id: "01KHZ6D9SWTJKNHPPWX68BHARE"
name: "admin_can_manage_profile_fields"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/profile_fields_controller.rb`
- `app/controllers/admin/profile_field_groups_controller.rb`
- `app/models/profile_field.rb`
- `app/models/profile_field_group.rb`
- `app/services/profile_fields/add.rb`
- `app/services/profile_fields/remove.rb`
- `app/services/profile_fields/import_from_csv.rb`
- `app/views/admin/profile_fields/index.html.erb` (Template)
- `app/views/admin/profile_fields/_add_group_modal.html.erb` (Template)
- `app/views/admin/profile_fields/_add_profile_field_modal.html.erb` (Template)
- `app/views/admin/profile_fields/_edit_group_modal.html.erb` (Template)
- `app/views/admin/profile_fields/_grouped_profile_fields.html.erb` (Template)
- `app/views/admin/profile_fields/_profile_field_form.html.erb` (Template)
- `app/views/admin/profile_fields/_ungrouped_profile_fields.html.erb` (Template)
- `spec/requests/admin/profile_fields_spec.rb` (Test)
- `spec/requests/admin/profile_field_groups_spec.rb` (Test)
- `spec/models/profile_field_spec.rb` (Test)
- `spec/models/profile_field_group_spec.rb` (Test)
- `spec/services/profile_fields/add_spec.rb` (Test)
- `spec/services/profile_fields/import_from_csv_spec.rb` (Test)
- `spec/services/profile_fields/remove_spec.rb` (Test)
- `spec/system/admin/admin_manages_profile_fields_spec.rb` (Test)

## Functional Overview

Super-admins can manage profile fields and their organizational groups through the `/admin/customization/profile_fields` interface. Fields are categorized as `text_field` or `text_area` input types and assigned a `display_area` of either `header` or `left_sidebar`. Groups organize related fields and can be created, renamed, and deleted independently. Creating or deleting a field triggers `Profile.refresh_attributes!` so that the corresponding store accessor on the `Profile` model is immediately synchronized. A CSV import path (`ProfileFields::ImportFromCsv`) allows bulk-loading fields, auto-creating groups as needed. The system enforces a hard limit of three fields in the `header` display area and requires each field label to be case-insensitively unique.

## Key Members

- `ProfileField#input_type` — enum: `text_field`, `text_area`
- `ProfileField#display_area` — enum: `header`, `left_sidebar`
- `ProfileField#show_in_onboarding` — boolean controlling whether the field appears during user onboarding
- `ProfileField#attribute_name` — auto-generated hex token used as the store accessor key on `Profile`
- `ProfileFieldGroup#profile_fields` — `has_many` with `dependent: :nullify` (fields become ungrouped when the group is deleted)
- `HEADER_FIELD_LIMIT` — constant set to 3; maximum number of fields with `display_area: header`

## Scenarios

### Admin creates a profile field group

1. An admin visits the profile fields admin page at `GET /admin/customization/profile_fields`.
2. The admin opens the "Add group" modal and submits a name and optional description.
3. `POST /admin/customization/profile_field_groups` creates a new `ProfileFieldGroup` record.
4. On success, a flash message confirms the group was created and the page redirects back to the index.

### Admin adds a profile field to a group

1. An admin opens the "Add Field" modal within an existing group on the index page.
2. The admin fills in label, description, placeholder text, input type, display area, and whether to show in onboarding.
3. `POST /admin/customization/profile_fields` invokes `ProfileFields::Add`, which creates a `ProfileField` record and calls `Profile.refresh_attributes!` to register the new store accessor.
4. On success, a flash message confirms creation and the page redirects to the index.
5. If creation fails (e.g., blank label or duplicate label), a flash error is shown instead.

### Admin updates a profile field or group

1. An admin expands the field or group entry and edits its attributes inline.
2. `PUT /admin/customization/profile_fields/:id` or `PUT /admin/customization/profile_field_groups/:id` updates the record directly.
3. On success, a flash message confirms the update and the page redirects to the index.

### Admin deletes a profile field

1. An admin clicks "Delete Profile Field" on a field entry and confirms the browser dialog.
2. `DELETE /admin/customization/profile_fields/:id` invokes `ProfileFields::Remove`, which destroys the record, undefines the store accessor methods on `Profile`, and calls `Profile.refresh_attributes!`.
3. A flash message confirms deletion and the page redirects to the index.

### Admin deletes a profile field group

1. An admin clicks "Delete Group" on a group header and confirms the browser dialog.
2. `DELETE /admin/customization/profile_field_groups/:id` destroys the `ProfileFieldGroup` record; its associated fields have their `profile_field_group_id` set to `nil` (nullified, not deleted).
3. A flash message confirms deletion and the page redirects to the index.

## Failures / Exceptions

- Creating or updating a field with a blank or duplicate label is rejected with a validation error flash.
- Attempting to assign `display_area: header` when three header fields already exist fails with `HEADER_LIMIT_MESSAGE` added to the record's errors.
- If `ProfileField#destroy` fails during removal, `ProfileFields::Remove` returns `success? false` and exposes `error_message` for the controller flash.
- If a `ProfileFieldGroup` fails to save or destroy, the controller renders a general error flash via `errors_as_sentence`.
