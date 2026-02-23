---
id: "01KJ41DVKVSHQT3TKSJP11Y7SZ"
name: "admin_can_create_tag"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/admin/tags_controller.rb`
- `app/models/tag.rb`
- `app/lib/constants/tags.rb`
- `app/views/admin/tags/new.html.erb` (Template)
- `app/views/admin/tags/_form.html.erb` (Template)
- `spec/requests/admin/tags_spec.rb` (Test)
- `spec/system/admin/admin_creates_new_tag_spec.rb` (Test)
- `spec/models/tag_spec.rb` (Test)
- `spec/factories/tags.rb` (Test)

## Functional Overview

A super admin can create a new tag through the admin interface by visiting the new tag form, filling in a name and optional attributes, and submitting. The controller forces the tag name to lowercase before saving. On success, the admin is redirected to the tag's edit page and shown a success flash. On failure, the form is re-rendered with validation errors displayed as a sentence. Before rendering the form, available badges are loaded for the badge association selector. The `Tag` model enforces that names are alphanumeric, at most 30 characters, and have a valid category; it also auto-converts markdown fields to HTML and normalizes color hex values before save.

## Design Intent

The name is forced to lowercase in the controller rather than relying solely on the model, ensuring uniform tag identity regardless of how the admin typed the input. Validation errors are formatted with `errors_as_sentence` and surfaced as a flash danger message to give the admin a clear, human-readable explanation of why the save failed.

## Key Members

- `ALLOWED_PARAMS` — whitelist of permitted tag attributes accepted by the controller
- `category` — required field; must be one of `ALLOWED_CATEGORIES` (`uncategorized`, `language`, `library`, `tool`, `site_mechanic`, `location`, `subcommunity`)
- `alias_for` — optional field; if set, must reference the name of an already-existing tag
- `bg_color_hex` / `text_color_hex` — optional hex color strings; validated against `HEX_COLOR_REGEXP`

## Scenarios

### Successful tag creation

1. A super admin visits the new tag page at `GET /admin/content_manager/tags/new`.
2. The controller initializes a blank `Tag` and loads all badges for the form's badge selector.
3. The admin fills in a name, optionally sets supported, short summary, badge, color values, and other attributes, then submits the form.
4. The controller downcases the name and calls `Tag#save`, which runs before-validation callbacks (markdown evaluation, summary sanitization, hex normalization) and model validations.
5. The tag is persisted, a success flash is set, and the admin is redirected to `edit_admin_tag_path` for the new tag.

### Failed tag creation due to validation errors

1. A super admin submits the new tag form with invalid data (e.g., a name containing special characters, an invalid hex color, or a missing/invalid category).
2. `Tag#save` returns false after model validations fail.
3. The controller sets a danger flash containing the validation errors formatted as a sentence and re-renders the `new` template so the admin can correct the form.

### Tag creation with alias

1. A super admin submits the new tag form with an `alias_for` value set to an existing tag's name.
2. The model's `validate_alias_for` callback confirms a tag with that name already exists.
3. If valid, the tag is saved and the admin is redirected to the edit page; if the referenced tag does not exist, a validation error is added and the form is re-rendered.

## Failures / Exceptions

- Name contains non-alphanumeric characters or exceeds 30 characters: validation fails, form re-rendered with error message.
- `bg_color_hex` or `text_color_hex` does not match `HEX_COLOR_REGEXP`: validation fails.
- `alias_for` refers to a tag name that does not exist: `validate_alias_for` adds an error and the save is rejected.
- Category is absent or not in `ALLOWED_CATEGORIES`: `validates :category, presence: true, inclusion:` fails the save.
