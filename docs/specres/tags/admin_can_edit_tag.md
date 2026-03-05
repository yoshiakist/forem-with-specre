---
id: "01KJ41RETE70D2JDJEGS0STSGM"
name: "admin_can_edit_tag"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/admin/tags_controller.rb`
- `app/models/tag.rb`
- `app/models/tag_subforem_relationship.rb`
- `app/workers/tags/alias_retag_worker.rb`
- `app/assets/javascripts/initializers/initializeAllTagEditButtons.js`
- `app/views/admin/tags/edit.html.erb` (Template)
- `app/views/admin/tags/_form.html.erb` (Template)
- `spec/requests/admin/tags_spec.rb` (Test)
- `spec/system/admin/admin_updates_tag_spec.rb` (Test)
- `spec/models/tag_spec.rb` (Test)
- `spec/models/tag_subforem_relationship_spec.rb` (Test)

## Functional Overview

Administrators can view and update the attributes of any existing tag through the admin interface. The edit page loads the tag's current state along with its associated moderators and subforem assignments, then renders a form exposing editable fields such as supported status, suggested flag, alias, display colors, badge, rules, submission template, and wiki body. On submission the controller validates and persists the changes, synchronizes subforem relationships (adding newly selected subforems and removing deselected ones), enqueues `Tags::AliasRetagWorker` asynchronously when the alias field is changed so that all tagged content is retagged to the preferred name, logs the action via `Audit::Logger`, and redirects back to the edit page with a success or error flash. The JavaScript initializer `initializeAllTagEditButtons` additionally controls visibility of the admin and tag-moderator edit buttons on the public tag page based on the current user's roles.

## Design Intent

Subforem relationships are managed with an explicit find-or-create/destroy pattern rather than replacing the full set atomically. This preserves existing relationship records for unchanged subforems and avoids unnecessary deletes. The alias retag job is throttled to a concurrency of one and placed on the low-priority queue to avoid overwhelming the system when a popular tag is aliased and has many associated articles.

## Key Members

- `ALLOWED_PARAMS` — whitelist of tag attributes the admin form is permitted to submit, preventing mass-assignment of sensitive fields
- `alias_for` — when set to an existing tag's name, marks this tag as an alias and triggers `Tags::AliasRetagWorker` to rewrite all taggings to use the canonical tag
- `subforem_ids` — array of subforem IDs submitted from the form; drives the sync of `TagSubforemRelationship` records

## Scenarios

### Admin loads the edit form

1. A super-admin navigates to the edit URL for a tag (e.g., `GET /admin/content_manager/tags/:id/edit`).
2. The controller fetches the tag, all available subforems, the IDs of subforems currently associated with the tag, and any users holding the `tag_moderator` role for that tag.
3. The edit template renders a moderator management section and an edit-details form pre-populated with the tag's current attribute values.

### Admin updates tag attributes

1. The admin modifies one or more fields in the form (e.g., toggles "Supported", changes the background color, edits the wiki body) and submits.
2. The controller applies the permitted parameters to the tag and saves.
3. On success, a flash message confirms the update and the admin is redirected back to the same edit page.
4. On validation failure, a flash error is shown and the admin remains on the edit page.

### Admin sets an alias for a tag

1. The admin enters an existing tag name in the alias field and submits the form.
2. The tag is saved with the `alias_for` value pointing to the canonical tag.
3. The controller detects that `alias_for` was set and enqueues `Tags::AliasRetagWorker` with the tag's ID.
4. The worker iterates over all taggings for the alias tag and updates each taggable object's tag list, replacing the alias with the canonical name.

### Admin manages subforem assignments

1. The admin checks or unchecks subforem checkboxes in the form and submits.
2. After saving tag attributes, the controller creates `TagSubforemRelationship` records for newly selected subforems (using find-or-create to avoid duplicates) and destroys relationships for subforems that were deselected.

### Tag-edit button visibility on the public tag page

1. On page load, `initializeAllTagEditButtons` reads the current user's admin and moderator-for-tags data.
2. If the user is an admin, the admin button (`tag-admin-button`) is made visible.
3. If the user is an admin or is listed as a moderator for the current tag, the edit button (`tag-edit-button`) and moderator button (`tag-mod-button`) are made visible.

## Failures / Exceptions

- If any tag attribute fails validation (e.g., `bg_color_hex` or `text_color_hex` does not match `HEX_COLOR_REGEXP`, `alias_for` references a non-existent tag, `category` is not in `ALLOWED_CATEGORIES`), the update is rolled back, an error flash is set, and the admin is redirected back to the edit page without changes being persisted.
- `Tags::AliasRetagWorker` silently skips processing if the tag record no longer exists when the job runs.
