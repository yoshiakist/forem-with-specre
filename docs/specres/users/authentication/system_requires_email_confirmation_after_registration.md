---
id: "01KJBK4DJZ9CXYE23MDH6TXZS3"
name: "system_requires_email_confirmation_after_registration"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/confirmations_controller.rb`
- `app/mailers/devise_mailer.rb`
- `app/views/devise/confirmations/new.html.erb` (Template)
- `app/views/devise/mailer/confirmation_instructions.html.erb` (Template)
- `app/views/devise/mailer/_creator_confirmation_instructions.html.erb` (Template)
- `spec/system/authentication/user_request_confirmation_spec.rb` (Test)
- `spec/mailers/devise_mailer_spec.rb` (Test)

## Functional Overview

After registration, the system requires users to confirm their email address before they can access the platform. A confirmation email is sent containing a unique token link. When the user clicks that link, the system verifies the token, signs the user in, and redirects them — to the creator setup page if they are a Forem creator, or to the standard post-confirmation destination otherwise. If the token is invalid, the confirmation request form is re-rendered with an error. Users who did not receive the email can request a resend from the confirmation page; the system always responds with a generic flash message regardless of whether the address is on file, preventing user enumeration. The email's sender name, subject, and confirmation URL hostname are scoped to the user's onboarding subforem, and creators receive a distinct email template.

## Scenarios

### Successful email confirmation

1. User registers an account and is directed to the confirmation pending page.
2. System sends a confirmation email with a unique token link to the user's address.
3. User clicks the confirmation link in the email.
4. System verifies the token, signs the user in, and sets a success flash notice.
5. If the user is a Forem creator, they are redirected to the creator setup page; otherwise they are redirected to the standard post-confirmation destination.

### Confirmation with invalid or expired token

1. User visits a confirmation URL with an invalid or expired token.
2. System attempts token verification, which fails, leaving errors on the resource.
3. System re-renders the confirmation request form with unprocessable entity status.

### User requests email resend

1. User on the confirmation pending page clicks the "Click here" prompt because no email arrived.
2. A resend form appears requesting their email address.
3. User submits the form with their email.
4. System attempts to send confirmation instructions, then clears all errors to avoid leaking account existence.
5. System re-renders the confirmation page with a generic flash message referencing the community contact email.

### Creator receives a distinct confirmation email

1. A newly registered creator account triggers confirmation email dispatch.
2. System detects the creator role and renders the creator-specific email partial.
3. The email instructs the creator to confirm so they can set up their Forem instance.

### Confirmation email is scoped to the user's subforem

1. A user registered through a specific subforem has an `onboarding_subforem_id` set.
2. System looks up the subforem's domain and community name for that ID.
3. Confirmation email is sent with the subforem's community name as sender and in the subject; the confirmation link hostname is set to the subforem's domain.
4. If no subforem association exists, the default subforem domain and community name are used as fallback.

## Failures / Exceptions

- Token verification failure causes re-render of the confirmation form with errors (unprocessable entity status).
- All resource errors are cleared before re-rendering on resend to prevent user enumeration (paranoid mode).
- If subforem database tables are unavailable (statement invalid or no database), the mailer falls back to `Settings::General.app_domain` or `ApplicationConfig["APP_DOMAIN"]` for URL generation.
- A user's display name containing a URL (e.g., includes "http") is excluded from the email greeting to prevent link injection; the greeting defaults to "Welcome!" in that case.
