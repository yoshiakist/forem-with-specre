---
id: "01KJ72CC7Y6GB7EXY8MNPEX2VQ"
name: "system_sends_email_confirmation_instructions"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/devise_mailer.rb`
- `app/views/devise/mailer/confirmation_instructions.html.erb` (Template)
- `app/views/devise/mailer/_creator_confirmation_instructions.html.erb` (Template)
- `spec/mailers/devise_mailer_spec.rb` (Test)
- `spec/mailers/previews/devise/mailer_preview.rb` (Test)

## Functional Overview

When a user registers or requests email re-confirmation, the system sends a confirmation email via `DeviseMailer#confirmation_instructions`. The email is personalized based on the recipient's role and subforem context: Forem creators receive a distinct template prompting them to set up their Forem Instance, while regular users receive a standard welcome message with a "Confirm my account" link. The sender name, subject line, and confirmation URL hostname are all resolved against the user's `onboarding_subforem_id`, falling back to the default subforem domain and community name when no subforem is assigned or when the assigned subforem cannot be found.

## Design Intent

Security emails opt out of Ahoy click tracking (`save_ahoy_options`) to avoid leaking confirmation tokens through redirect tracking URLs. Subforem-aware URL generation ensures recipients click a link on the correct domain for their community, which is important when a Forem hosts multiple independent subforems under different hostnames. The name sanitization (suppressing display when the name contains "http") prevents accidental link injection in the greeting.

## Key Members

- `@name` — the recipient's display name, used in the greeting; suppressed if it contains a URL scheme
- `@resource` — the Devise resource (User) being confirmed
- `@subforem_id` — resolved from the user's `onboarding_subforem_id`; drives URL host and community name lookup
- `@subforem_domain` — the hostname used for the confirmation URL; resolved via `Subforem.cached_id_to_domain_hash`
- `confirmation_token` — the one-time token appended to the confirmation URL as a query parameter
- `opts[:subject]` — built as `"#{name}, confirm your #{community_name} account"`

## Scenarios

### Forem creator confirmation

1. A user with the `creator` role registers or requests confirmation.
2. The mailer sets `@resource` and resolves subforem context.
3. The subject is set to `"#{name}, confirm your #{community_name} account"` using the subforem-specific community name.
4. The email renders the `_creator_confirmation_instructions` partial, which includes the message: "Hello! Once you've confirmed your email address, you'll be able to setup your Forem Instance."
5. The confirmation URL in the button uses the resolved subforem domain and includes `confirmation_token` as a query parameter.

### Regular user confirmation

1. A non-creator user registers or requests confirmation.
2. The mailer sets `@resource` and resolves subforem context.
3. The subject is set to `"#{name}, confirm your #{community_name} account"`.
4. The email renders the standard body: a welcome greeting ("Welcome [Name]!") followed by "You can confirm your account email through the link below:" and a "Confirm my account" link.
5. The confirmation URL includes the resolved subforem domain and `confirmation_token` as a query parameter.

### Name contains a URL — greeting sanitization

1. The user's display name contains "http" (e.g., a URL was entered as a name).
2. The mailer detects the URL in the name and suppresses the personalized greeting.
3. The greeting renders as "Welcome!" without the name, preventing link injection in the email body.

### Subforem-specific branding

1. The user has a valid `onboarding_subforem_id` that maps to a known subforem.
2. The mailer resolves the subforem's domain from `Subforem.cached_id_to_domain_hash`.
3. The subforem-specific community name is fetched via `Settings::Community.community_name(subforem_id:)`.
4. The sender address is set to `"#{subforem_community_name} <#{from_email_address}>"`.
5. The subject and confirmation URL hostname both reflect the subforem's identity.

### No subforem assigned — default fallback

1. The user has no `onboarding_subforem_id` (nil).
2. The mailer falls back to `Subforem.cached_default_domain` for the confirmation URL host.
3. The sender and subject use the default community name from `Settings::Community.community_name`.

### Invalid subforem ID — graceful fallback

1. The user's `onboarding_subforem_id` does not correspond to any known subforem.
2. The mailer falls back to the default subforem domain and default community name, as if no subforem were assigned.

## Failures / Exceptions

- If the subforem domain already includes a port number (e.g., `dev.example.com:3000`) and the Rails environment appends a port, the mailer avoids duplicating the port (e.g., no `dev.example.com:3000:3000`).
- When multiple users with different subforem assignments receive confirmation emails in the same process, each email is independently resolved — subforem context does not leak between deliveries.
