---
id: "01KJBKJDQQWQES8PHFHKT13XAF"
name: "user_can_reset_password"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/passwords_controller.rb`
- `app/mailers/devise_mailer.rb`
- `app/views/devise/passwords/new.html.erb` (Template)
- `app/views/devise/passwords/edit.html.erb` (Template)
- `app/views/devise/mailer/reset_password_instructions.html.erb` (Template)
- `app/views/users/_account_set_password.html.erb` (Template)
- `spec/requests/user/user_changes_password_spec.rb` (Test)
- `spec/system/user_logs_in_with_password_spec.rb` (Test)
- `spec/mailers/devise_mailer_spec.rb` (Test)

## Functional Overview

A user who has forgotten their password can request a reset email from the login page. The system sends an email containing a tokenized link to the user's registered address. Following the link opens a form where the user sets a new password. Already-signed-in users may also access this flow. After a successful reset, the user is redirected to the page they were on before initiating the request. Authenticated users may alternatively change their password directly through account settings without going through the email flow.

## Design Intent

The controller extends Devise's built-in `PasswordsController` and removes the `require_no_authentication` guard so that already-signed-in users can still trigger a reset. After the reset email is sent, the controller redirects back to the HTTP referrer (stored in session), rather than always forwarding to a fixed path, so the user ends up where they started.

## Scenarios

### User requests a password reset email

1. User visits the "Forgot password" page via `/users/password/new`.
2. User enters their registered email address and submits the form.
3. System enqueues a `reset_password_instructions` email addressed to the user.
4. The email is sent from the community's configured sender address, with the community's reply-to address.
5. The email contains a link with a one-time reset token pointing to the `edit_password` URL.
6. System shows a confirmation notice and redirects the user back to the page they came from.

### User follows the reset link and sets a new password

1. User clicks the link in the reset email, which includes the `reset_password_token` parameter.
2. System renders the "Change your password" form, pre-populating the hidden token field.
3. User enters a new password (8+ characters) and confirms it, then submits.
4. System validates the token, updates the password, and signs the user in.
5. User is redirected to the home page.

### Already-signed-in user requests a reset

1. A signed-in user navigates to `/users/password/new`.
2. Because `require_no_authentication` is skipped, the form is shown without redirecting them away.
3. The flow proceeds identically to the unauthenticated case.

### User sets a new password directly from account settings

1. Signed-in user navigates to account settings and finds the "Password" section.
2. User enters their current password, a new password, and the confirmation.
3. System validates all three fields and updates the password on success, redirecting to `/settings/account`.

### Invalid or expired reset token

1. User follows a reset link with a token that is expired or has already been used.
2. System rejects the request and displays a validation error on the edit-password form.

## Failures / Exceptions

- Submitting a wrong current password from the settings form returns "Current password is invalid".
- A new password shorter than 8 characters returns "Password is too short (minimum is 8 characters)".
- A mismatched new password and confirmation returns a validation error indicating the confirmation does not match.
- The reset email link does not include Ahoy click-tracking parameters, preventing analytics interference with the token URL.
