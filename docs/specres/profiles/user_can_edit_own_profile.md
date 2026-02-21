---
id: "01KHZ69F0GE1R07TXK53AAA1K8"
name: "user_can_edit_own_profile"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/profiles_controller.rb`
- `app/models/profile.rb`
- `app/validators/profile_validator.rb`
- `app/decorators/profile_decorator.rb`
- `app/helpers/profile_helper.rb`
- `app/views/users/_profile.html.erb` (Template)
- `spec/requests/profiles_request_spec.rb` (Test)
- `spec/models/profile_spec.rb` (Test)
- `spec/system/user/user_edits_profile_spec.rb` (Test)
- `spec/helpers/profile_helper_spec.rb` (Test)

## Functional Overview

An authenticated user can edit their own profile by submitting the profile settings form at `/settings/profile`. The form allows updating user-level fields (name, email, username, profile image), static profile fields (summary/bio, location, website URL), admin-configured dynamic `ProfileField` entries stored in the profile's `data` JSON column, and user settings (display email on profile, brand color). On a successful `PUT /profiles/:id` request, the system delegates to `Users::Update` and redirects to the settings page with a success notice. On failure, the form is re-rendered with inline error messages. After a successful save, the system asynchronously busts the profile details cache and, when relevant, enqueues a spam check.

## Design Intent

Profile attributes are split into three namespaces in the form (`user`, `profile`, `users_setting`) and the controller applies strict allowlists for each namespace, ensuring users cannot mass-assign unauthorized attributes. Dynamic profile fields are stored in a JSON `data` column via `store_accessor`, allowing admins to add new fields without schema migrations. Validation is extracted into `ProfileValidator` so length and format rules are enforced consistently across both static and dynamic fields.

## Key Members

- `Profile::STATIC_FIELDS` — `["summary", "location", "website_url"]`; always-present columns validated directly on the model.
- `ProfileValidator::MAX_SUMMARY_LENGTH` — 200 characters; the summary field has a grandfathering rule that exempts users whose previous summary already exceeded the limit.
- `ProfileValidator::MAX_TEXT_AREA_LENGTH` — 200 characters for dynamic text-area fields (newlines collapsed before counting).
- `ProfileValidator::MAX_TEXT_FIELD_LENGTH` — 100 characters for dynamic text-field fields.
- `ProfilesController::ALLOWED_USER_PARAMS` — `[:name, :email, :username, :profile_image]`.
- `ProfilesController::ALLOWED_USERS_SETTING_PARAMS` — `[:display_email_on_profile, :brand_color1]`.

## Scenarios

### Successful profile update

1. A signed-in user navigates to `/settings/profile` and edits one or more fields (e.g., name, bio, location).
2. The user clicks Save, submitting a `PUT /profiles/:id` request.
3. `ProfilesController#update` permits params across the `user`, `profile`, and `users_setting` namespaces and calls `Users::Update`.
4. `Users::Update` persists the changes; the `Profile` model runs `ProfileValidator` and model-level validations before saving.
5. On success, the user is redirected to `user_settings_path` and a success flash notice is displayed.
6. After commit, `Users::BustProfileDetailsCacheWorker` is enqueued if summary, location, website URL, social image, or any `data` field changed.

### Validation failure (invalid input)

1. A signed-in user submits a profile update with invalid data (e.g., a username containing spaces, a bio exceeding 200 characters, or a malformed website URL).
2. `ProfileValidator` or model-level validations add errors to the record.
3. `Users::Update` returns a failure result containing the error messages.
4. The controller re-renders `users/edit` with the profile tab active and displays the errors inline via a flash error message.

### Unauthenticated access attempt

1. A visitor who is not signed in sends a `PATCH /profiles/:id` request.
2. The `authenticate_user!` before-action intercepts the request and redirects to the login page (`new_magic_link_path`).

### Editing dynamic admin-configured profile fields

1. An admin has created `ProfileField` records (e.g., "Preferred Ice Cream Flavor") grouped under a `ProfileFieldGroup`.
2. When the signed-in user visits `/settings/profile`, these fields are rendered dynamically from the database.
3. The user fills in values for the dynamic fields and saves.
4. The values are stored in the `Profile#data` JSON column via auto-defined accessors, and reflected on the user's public profile page in the appropriate display area (e.g., left sidebar or header).

### Profile spam check on save

1. A signed-in user updates their website URL or enters a summary containing spam trigger terms.
2. After the profile is saved, the `after_commit` callback fires and enqueues `Users::HandleProfileSpamWorker` for asynchronous spam review.

## Failures / Exceptions

- **Summary too long**: Adding a bio longer than 200 characters is rejected unless the user's previous summary was already over the limit (grandfathering rule).
- **Website URL invalid**: URLs without a scheme (`http`/`https`) or pointing to localhost are rejected with a "not a valid URL" error.
- **Dynamic field too long**: Text-area dynamic fields exceeding 200 characters (after collapsing newlines) or text-field dynamic fields exceeding 100 characters are rejected with a field-specific error.
- **Invalid username**: Usernames containing spaces or other disallowed characters cause `Users::Update` to return a failure, and the form is re-rendered with the error message.
