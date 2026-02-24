---
id: "01KJ759KKVVQ8YQZP1B78QC3Q6"
name: "user_can_verify_account_ownership_via_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/email_authorization.rb`
- `app/controllers/email_authorizations_controller.rb`
- `app/mailers/verification_mailer.rb`
- `app/javascript/packs/confirmationEmail.js`
- `app/controllers/admin/users_controller.rb`
- `app/views/mailers/verification_mailer/account_ownership_verification_email.html.erb` (Template)
- `app/views/mailers/verification_mailer/account_ownership_verification_email.text.erb` (Template)
- `app/views/admin/users/show/emails/_verification.html.erb` (Template)
- `spec/models/email_authorization_spec.rb` (Test)
- `spec/factories/email_authorizations.rb` (Test)
- `spec/requests/admin/users_spec.rb` (Test)

## Functional Overview

When an admin needs to confirm that a user still controls their registered email address, the admin panel provides an action to send a verification email. The system creates an `EmailAuthorization` record of type `account_ownership` with a unique, auto-generated confirmation token, then sends the user an email containing a verification link. The user proves ownership by clicking the link, which validates the token against the most recent `EmailAuthorization` for that username and records a `verified_at` timestamp. Admins can also resend Devise confirmation instructions to unconfirmed users, or manually mark a user's email as confirmed, with both actions producing an audit note.

## Design Intent

The `sent_at` alias for `created_at` on `EmailAuthorization` keeps the verification-token lifecycle model uniform across all authorization types (`merge_request`, `account_lockout`, `uuid_issue`, `account_ownership`) without requiring a separate column. Only the most recently created token for a user is checked during verification, so re-triggering the flow invalidates prior tokens implicitly. The admin panel conditionally shows confirmation vs. re-verification actions depending on whether the user's email is already confirmed by Devise, preventing misuse of the wrong flow.

## Key Members

- `EmailAuthorization#confirmation_token` — URL-safe base64 token auto-generated on create; compared verbatim during the verify step
- `EmailAuthorization#verified_at` — set to the current timestamp when the user successfully clicks the verification link; `nil` until then
- `EmailAuthorization#type_of` — must be one of `merge_request`, `account_lockout`, `uuid_issue`, `account_ownership`; this flow uses `account_ownership`
- `EmailAuthorization.last_verification_date(user)` — returns the `verified_at` of the most recent verified authorization for a user, used by the admin panel to show the last verification date

## Scenarios

### Admin sends a verification email to a confirmed user

1. Admin visits the user's admin page; the user's email is already confirmed via Devise.
2. The panel shows a "Send verification email" button (or "Re-verify" if previously verified).
3. Admin clicks the button, triggering `verify_email_ownership`.
4. The system creates a new `EmailAuthorization` record with `type_of: "account_ownership"` and a fresh token, then delivers the verification email immediately.
5. A success flash message is displayed and the admin is redirected back to the user page.

### User confirms account ownership via the emailed link

1. The user receives an email with a "click here" link embedding their username and the confirmation token.
2. The user clicks the link, which hits `GET /email_authorizations/verify` with `username` and `confirmation_token` params.
3. The controller confirms the authenticated user matches the username in the URL, then fetches that user's most recent `EmailAuthorization`.
4. If the token matches, `verified_at` is set to the current time and the user is redirected to the home page.

### Admin resends Devise confirmation instructions to an unconfirmed user

1. The user's email is not yet Devise-confirmed, so the panel shows a "Send confirmation" button instead.
2. Admin clicks it, triggering `send_email_confirmation`.
3. The system calls Devise's `send_confirmation_instructions` on the user.
4. On success, a flash message confirms the email was sent; on failure, an error flash is shown.

### Admin manually confirms a user's email

1. On the unconfirmed-user panel, the admin clicks "Mark as Confirmed".
2. The `confirm_email` action calls Devise `confirm` on the user.
3. If successful, a `Note` record is created documenting the action and the admin who performed it, and a success response is returned.

### User opens "Didn't get the email?" modal

1. After a verification email has been sent, the page includes a button with class `js-confirmation-button`.
2. The user clicks it; `confirmationEmail.js` opens a modal titled "Didn't get the email?" using `window.Forem.showModal`.
3. The user can dismiss the modal by clicking any element with class `js-dismiss-button` (the second one, if multiple are present), which calls `window.Forem.closeModal`.

## Failures / Exceptions

- If the authenticated user does not match the `username` parameter in the verify URL, the controller raises `ActionController::RoutingError` ("Not Found").
- If the submitted `confirmation_token` does not match the most recent `EmailAuthorization` token, the same routing error is raised.
- If `send_confirmation_instructions` returns a falsy value, the admin receives an error flash and a 503 JSON response (for JS callers).
- If `VerificationMailer` delivery fails, the admin receives an error flash and a 503 JSON response.
