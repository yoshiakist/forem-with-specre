---
id: "01KJ9R7RN71B1E3T8PRGBS19JC"
name: "user_changes_password"
status: "draft"
---

## Related Files

- `app/views/users/_account_set_password.html.erb` (Template)

## Functional Overview

Authenticated users can change their account password through the settings page. The form requires the user to supply their current password for verification, followed by a new password and a confirmation of that new password. A link to the forgot-password flow is also surfaced for users who cannot remember their current password. On submission the form posts to `user_update_password_path`, where the server validates all three fields before applying the change.

## Design Intent

Requiring the current password before accepting a new one guards against session hijacking: even if an attacker gains access to an unlocked browser, they cannot silently rotate the credential without already knowing it. The forgot-password link provides a safe escape hatch without weakening this protection.

## Scenarios

### Successful password change

1. The authenticated user navigates to the account settings page and locates the password section.
2. The user enters their correct current password, a new password, and the same new password in the confirmation field.
3. The user submits the form.
4. The system verifies the current password, updates the credential, and confirms success to the user.

### Wrong current password

1. The user enters an incorrect value in the current password field along with a new password and confirmation.
2. The user submits the form.
3. The system rejects the request and displays an error indicating the current password is wrong; the password is not changed.

### New password and confirmation do not match

1. The user enters a valid current password but types different values in the new password and confirmation fields.
2. The user submits the form.
3. The system rejects the request and indicates the new password and its confirmation must be identical; the password is not changed.

### Missing required field

1. The user leaves one or more of the three fields empty and attempts to submit the form.
2. Browser-level required-field validation prevents submission and prompts the user to complete the missing field(s).

### User does not know their current password

1. The user clicks the forgot-password link displayed in the section description.
2. The system redirects the user to the password-reset flow where they can recover access via their registered email address.

## Failures / Exceptions

- If the current password field is empty, the form will not submit due to the `required` attribute.
- If the new password or confirmation field is empty, the form will not submit due to the `required` attribute.
- When the server rejects the request (wrong current password or mismatched confirmation), the password remains unchanged and the user sees an appropriate error message.
