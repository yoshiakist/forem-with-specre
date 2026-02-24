---
id: "01KJ729K8JA4QKFYMSJEHH7DT5"
name: "system_sends_account_verification_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/verification_mailer.rb`
- `spec/mailers/verification_mailer_spec.rb` (Test)
- `spec/mailers/previews/verification_mailer_preview.rb` (Test)
- `app/views/mailers/verification_mailer/account_ownership_verification_email.html.erb` (Template)
- `app/views/mailers/verification_mailer/account_ownership_verification_email.text.erb` (Template)

## Functional Overview

When account ownership verification is requested for a user, the system sends a transactional email that contains a unique confirmation link. The email is addressed to the user's registered email address and branded with the community name and sender address resolved from the user's associated subforem (or the default subforem if none is set). A one-time `EmailAuthorization` record of type `account_ownership` is created to generate the confirmation token, which is embedded into the verification link in both the HTML and plain-text versions of the email body.

## Key Members

- `@user` — the User record looked up by `user_id` from mailer params; determines the recipient address and username shown in the body
- `@confirmation_token` — single-use token stored on the `EmailAuthorization` record and embedded in the verification URL
- `@subforem_id` — resolved from the user's `onboarding_subforem_id`; drives community name and domain used in the subject, from header, and verification link

## Scenarios

### Standard account ownership verification email

1. The system looks up the user by the provided `user_id`.
2. A new `EmailAuthorization` record of type `account_ownership` is created for that user, producing a unique confirmation token.
3. The email is sent to the user's registered address with:
   - a subject that includes the community name (e.g., "Verify your ownership of your <Community> account")
   - a `From` header formatted as "<Community Name> Email Verification <noreply@...>"
   - an HTML and plain-text body containing a link to the email verification path, with the confirmation token and username embedded as query parameters

### Subforem-branded email

1. When the user has an `onboarding_subforem_id`, the mailer resolves the community name and sender domain using that subforem's configuration.
2. The email subject and `From` header display the subforem's community name instead of the default community name.
3. The verification link in the email body uses the subforem's domain as the URL host.

### Plain-text fallback

1. Both HTML and plain-text multipart variants are rendered.
2. The plain-text body presents the same greeting, explanatory copy, and verification URL in unformatted text, so recipients with plain-text clients receive a fully functional email.
