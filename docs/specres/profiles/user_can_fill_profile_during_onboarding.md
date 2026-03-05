---
id: "01KHZ6CFQNFQRAFDNMEDQ8X9S0"
name: "user_can_fill_profile_during_onboarding"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/profile_field_groups_controller.rb`
- `app/javascript/onboarding/components/ProfileForm.jsx`
- `app/javascript/onboarding/components/ProfileForm/CheckBox.jsx`
- `app/javascript/onboarding/components/ProfileForm/ProfileImage.jsx`
- `app/javascript/onboarding/components/ProfileForm/TextArea.jsx`
- `app/javascript/onboarding/components/ProfileForm/TextInput.jsx`
- `app/views/profile_field_groups/index.json.jbuilder` (Template)
- `app/javascript/onboarding/components/__tests__/ProfileForm.test.jsx` (Test)
- `app/javascript/onboarding/components/__tests__/ProfileImage.test.jsx` (Test)
- `spec/requests/profile_field_groups_request_spec.rb` (Test)

## Functional Overview

During onboarding, the user is presented with a "Build your profile" form that fetches profile field groups from `GET /profile_field_groups?onboarding=true`. The server filters the groups to include only those with fields marked for onboarding, and simultaneously records that the user has seen the onboarding screen and accepted the code of conduct and terms of service. The form renders fixed fields for profile image, name, username, and bio, followed by any dynamically loaded field groups. Each field group can contain text inputs, text areas, or checkboxes. When the user submits, the collected values are sent to `PATCH /onboarding`, advancing them to the next onboarding step. The form tracks whether all fields are empty to determine if the user may skip instead of continuing.

## Scenarios

### Loading onboarding profile fields

1. When the `ProfileForm` component mounts, it calls `GET /profile_field_groups?onboarding=true`.
2. The server filters profile field groups to return only groups that contain at least one field tagged for onboarding, and marks the user's `saw_onboarding`, `checked_code_of_conduct`, and `checked_terms_and_conditions` flags as true.
3. The response JSON contains each group's `id`, `name`, `description`, and an array of `profile_fields` (each with `attribute_name`, `label`, `input_type`, `placeholder_text`, and `description`).
4. The component renders the returned groups as sections below the fixed fields, with each field rendered as a `TextInput`, `TextArea`, or `CheckBox` according to its `input_type`.

### Filling in fixed profile fields

1. The user sees fixed fields for profile image, name (max 50 characters), username (max 20 characters), and bio (max 200 characters, with a live character counter).
2. The user types into any field; each keystroke triggers `handleFieldChange`, which updates the form's internal state.
3. If all field values in the form become empty, the navigation changes to allow skipping; otherwise the Continue button remains active.

### Uploading a profile image

1. The user clicks "Edit profile image" and selects an image file (any image type, max 25 MB).
2. The component shows a spinner with "Uploading..." text while the upload is in progress.
3. On success, the new image URL is stored in component state and the image preview updates.
4. If the upload fails, an error message is displayed below the upload control and the spinner is removed.

### Submitting the profile form

1. The user clicks Continue; the component sends `PATCH /onboarding` with the user's `name`, `username`, `profile_image_90`, and `last_onboarding_page`, plus all dynamic profile field values under a separate `profile` key.
2. On a successful response, `next()` is called to advance to the following onboarding step.
3. If the server responds with HTTP 422, the returned `errors` value is displayed in an alert banner above the form.
4. For any other failure, a generic error message "Unable to continue, please try again." is displayed and the error is reported to Honeybadger.

## Failures / Exceptions

- If the initial fetch of profile field groups fails (network error or non-OK response), the component sets an error state and displays an error message.
- If the profile image upload fails, an upload error message is shown inline beneath the image uploader; the form remains usable.
- If the form submission fails with HTTP 422, the server-provided error string is shown in a danger notice; for other errors a generic fallback message is shown.
