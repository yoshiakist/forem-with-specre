---
id: "01KJ72CN8M7DDPD8AGN754MKTK"
name: "system_sends_invitation_instructions_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/devise_mailer.rb` (Source)
- `app/views/devise/mailer/invitation_instructions.html.erb` (Template)
- `app/views/devise/mailer/invitation_instructions.text.erb` (Template)
- `spec/mailers/devise_mailer_spec.rb` (Test)
- `spec/mailers/previews/devise_invitable/mailer_preview.rb` (Test)

## Functional Overview

When an administrator invites a user to the platform, the system sends an invitation instructions email via `DeviseMailer#invitation_instructions`. The email subject, body message, and footnote are all customizable through options passed at call time. If no custom subject is provided, the email falls back to the default subject "Invitation Instructions". The body renders a styled acceptance link and, optionally, a due date for accepting the invitation. Custom message and footnote content are rendered as Markdown; when a custom message is present, the default Devise invitation copy is suppressed.

## Design Intent

The customization surface (subject, message, footnote) allows platform operators to tailor invitation emails for different contexts — such as community onboarding campaigns — without requiring code changes. Falling back to the default subject when none is supplied ensures the email is always deliverable and recognizable even when the caller omits optional fields. Rendering custom content as Markdown gives operators rich-text formatting without exposing raw HTML injection.

## Key Members

- `opts[:custom_invite_subject]` — Optional subject line. When present and non-blank, replaces the default "Invitation Instructions" subject.
- `opts[:custom_invite_message]` — Optional body message rendered as Markdown. When present, suppresses the default Devise invitation copy (hello, someone-invited-you, accept-instructions paragraphs).
- `opts[:custom_invite_footnote]` — Optional footnote rendered as Markdown, shown below the acceptance link.
- `@token` — The invitation token embedded in the acceptance URL.
- `@resource.invitation_due_at` — When set, a due-date line is appended to the email body.

## Scenarios

### Invitation email with all custom fields provided

1. Caller invokes `DeviseMailer.invitation_instructions(user, token, opts)` with `custom_invite_subject`, `custom_invite_message`, and `custom_invite_footnote` all present in `opts`.
2. The mailer assigns the custom message to `@message` and the custom footnote to `@footnote`, then sets the subject header to the custom subject value.
3. The HTML template detects that `@message` is present and renders it as Markdown, skipping the default Devise invitation paragraphs.
4. The acceptance link is rendered as a styled button pointing to the accept-invitation URL containing the token.
5. The custom footnote is rendered as Markdown below the acceptance link.
6. The resulting email subject equals the custom subject value and the body contains both the custom message and the custom footnote.

### Invitation email with no custom subject (fallback to default)

1. Caller invokes `DeviseMailer.invitation_instructions(user, token, {})` with an empty options hash (no `custom_invite_subject` key).
2. The mailer evaluates `opts[:custom_invite_subject].presence`, which is nil/blank, and falls back to the literal string "Invitation Instructions".
3. The resulting email subject is "Invitation Instructions".

### Invitation email with no custom message (default Devise copy rendered)

1. Caller invokes the mailer without `custom_invite_message` in opts.
2. The HTML template detects that `@message` is blank and renders the default Devise i18n copy: the hello greeting, the "someone invited you" paragraph, and the accept-instructions line.
3. The acceptance link is still rendered as a styled button.

### Invitation email with an acceptance due date

1. The invited user's `invitation_due_at` attribute is set to a future timestamp.
2. The template detects this and renders a localized due-date line after the acceptance button.
3. When `invitation_due_at` is nil, the due-date line is omitted entirely.

## Failures / Exceptions

- If `custom_invite_subject` is present but blank (e.g., an empty string), `presence` returns nil and the subject falls back to "Invitation Instructions".
- The text-format template does not branch on `@message`; it always renders the default Devise i18n strings and the acceptance URL regardless of custom options. Custom message and footnote are not reflected in the plain-text part.
