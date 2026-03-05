---
id: "01KJ72D0HZ49WMGHS1ERWQEKVT"
name: "system_sends_magic_link_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/verification_mailer.rb`
- `app/views/mailers/verification_mailer/magic_link.html.erb`
- `app/views/mailers/verification_mailer/magic_link.text.erb`
- `spec/mailers/verification_mailer_spec.rb` (Test)
- `spec/mailers/previews/verification_mailer_preview.rb` (Test)

## Functional Overview

When a user requests a magic-link / passwordless sign-in, the system delivers a transactional email to that user's address. The email carries a short numeric `sign_in_token` displayed prominently as a copy-paste code, plus a direct magic-link URL the user can click on the same device. Subject, sender display name, and magic-link domain are all scoped to the subforem the user originally onboarded through; when no subforem is recorded, the system falls back to the default subforem's community name and domain. The reply-to address is set independently via `ForemInstance.reply_to_email_address`.

## Design Intent

Passwordless sign-in requires a credential delivery channel that is both phishing-resistant (the code is short and visible, not buried in a URL) and immediately actionable (the direct link covers the common same-device flow). Scoping branding and the link domain to the originating subforem preserves the user's mental model of the community they signed up for, avoiding confusion when multiple subforems share the same mail infrastructure.

## Key Members

- `params[:user_id]` — ID used to look up the recipient `User` record
- `@user.sign_in_token` — short alphanumeric token embedded in both the displayed code block and the magic-link URL; expires in 20 minutes
- `Settings::Community.community_name(subforem_id:)` — subforem-aware community name used in subject and sender display name
- `ForemInstance.from_email_address` — envelope sender address
- `ForemInstance.reply_to_email_address` — reply-to address set separately from the sender
- `magic_link_url(token)` — URL helper that builds the sign-in URL scoped to the subforem's domain

## Scenarios

### Standard magic-link delivery

1. A sign-in request is triggered for a user whose `onboarding_subforem_id` identifies a specific subforem.
2. The mailer looks up the user by `user_id` parameter.
3. It resolves the subforem's community name and domain.
4. The email is addressed to the user's registered email address.
5. The subject reads "Sign in to \<community name\> with a magic code".
6. The sender display name is "\<community name\> \<from email address\>".
7. The reply-to header is set to `ForemInstance.reply_to_email_address`.
8. The HTML body displays the `sign_in_token` as a prominent code block, followed by a direct magic-link URL pointing to the subforem's domain.
9. The plain-text body contains the user's name and the magic-link URL only.
10. The body does not include the generic "Not signed-in on this device?" copy.

### Subforem-specific branding

1. The user's `onboarding_subforem_id` is set to a non-default subforem.
2. `Settings::Community.community_name(subforem_id:)` returns that subforem's community name.
3. The email subject and sender display name both reflect the subforem's community name.
4. The magic-link URL in the body uses the subforem's domain.
5. The body also includes the subforem's community name.

### Nil onboarding_subforem_id (default subforem fallback)

1. The user's `onboarding_subforem_id` is nil.
2. The mailer resolves the subforem ID via `Subforem.cached_default_id`.
3. Subject and sender display name use the default subforem's community name.
4. The magic-link URL in the body uses the default subforem's domain.

## Failures / Exceptions

- If the `User` record cannot be found for the given `user_id`, `User.find` raises `ActiveRecord::RecordNotFound` and no email is sent.
- If `sign_in_token` is blank at preview time, `VerificationMailerPreview` writes a placeholder token via `update_column` to allow rendering without errors.
