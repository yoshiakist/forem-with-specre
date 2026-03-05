---
id: "01KJBK4CV4DXZ9SFQ9QVWB6YK2"
name: "user_can_register_with_email_and_password"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/registrations_controller.rb`
- `app/policies/registration_policy.rb`
- `app/mailers/devise_mailer.rb`
- `app/views/devise/registrations/new.html.erb` (Template)
- `app/views/devise/registrations/by_email.html.erb` (Template)
- `app/views/devise/registrations/_registration_form.html.erb` (Template)
- `app/views/shared/authentication/_email_registration_form.html.erb` (Template)
- `app/views/shared/authentication/_providers_registration_form.html.erb` (Template)
- `spec/requests/registrations_spec.rb` (Test)
- `spec/system/authentication/conditional_registration_spec.rb` (Test)
- `spec/mailers/devise_mailer_spec.rb` (Test)

## Functional Overview

A visitor can create a new Forem account by submitting their name, username, email address, password, and optionally a profile image through the email registration form. Before the account is created, the system checks that email registration is permitted by site settings and, when configured, validates a reCAPTCHA response. Emails must pass an optional domain allow-list check. On success the user's roles are initialized; if SMTP is enabled the user is redirected to an email-confirmation page without being signed in, otherwise they are signed in and redirected to the home feed. The very first user to register on a new Forem instance is treated as the creator/super-admin and is immediately signed in and directed to the admin creator settings. A subforem-aware confirmation email is sent that customizes the sender name, subject, and confirmation link domain based on the subforem the user signed up through.

## Design Intent

Email registration is an opt-in feature controlled by `Settings::Authentication.allow_email_password_registration`. The `RegistrationPolicy` enforces authorization before any account data is persisted, so misconfigured or disabled email sign-up raises a `Pundit::NotAuthorizedError` rather than silently failing. The `waiting_on_first_user` path bypasses the normal policy gate so that a brand-new Forem instance can bootstrap its first admin without prior configuration.

## Scenarios

### Successful registration when SMTP is disabled

1. Visitor navigates to the sign-up page; the system confirms they are not already signed in.
2. Visitor fills in name, username, email, password, and password confirmation, then submits the form.
3. System authorizes the request via `RegistrationPolicy` and passes reCAPTCHA validation (or skips it if not required).
4. System validates the email domain against the allow-list (if configured), assigns a random profile image when none is uploaded, and saves the new user record.
5. System assigns initial roles and signs the user in, then redirects them to the home feed.

### Successful registration when SMTP is enabled (email confirmation required)

1. Visitor submits valid registration credentials on a Forem where SMTP is configured.
2. System creates the user account and assigns initial roles but does not sign them in.
3. System redirects the visitor to the confirm-email page and Devise sends a confirmation email.
4. Confirmation email is addressed from the community name associated with the user's subforem, and the confirmation link domain matches that subforem.

### Registration blocked when email sign-up is disabled

1. Visitor attempts to POST to the registration endpoint on a Forem where email registration is disabled.
2. `RegistrationPolicy#create?` returns false; the system raises `Pundit::NotAuthorizedError` and the account is not created.

### Registration blocked by failed reCAPTCHA

1. Visitor submits the registration form without completing the reCAPTCHA challenge on a Forem that requires it.
2. System detects the missing or invalid reCAPTCHA response, sets a flash notice, and redirects back to the email sign-up form without creating an account.

### First-user (Forem creator) onboarding

1. Visitor accesses a Forem instance that has no users yet (`waiting_on_first_user` is true).
2. When `FOREM_OWNER_SECRET` is set in the environment, the visitor must supply the matching secret in the registration form.
3. On success the system creates the creator account, grants super-admin and trusted roles, creates the mascot account, clears the waiting-on-first-user flag, and enqueues the Discover registration worker.
4. Creator is signed in immediately and redirected to the admin creator settings page.

## Failures / Exceptions

- Submitting a password that does not match the confirmation leaves the account unpersisted and re-renders the `by_email` form with validation errors.
- Submitting an email address whose domain is not in the configured allow-list clears the email field and adds a domain error, preventing account creation.
- Visiting the sign-up page while already authenticated redirects immediately to the home feed.
- Accessing the sign-up page from a non-root subforem results in a permanent redirect (301) to the root subforem's `/enter` path.
