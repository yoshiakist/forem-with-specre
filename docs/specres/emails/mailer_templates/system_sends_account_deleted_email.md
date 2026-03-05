---
id: "01KJ72PJ45D3ZFHQBYBXD9EEME"
name: "system_sends_account_deleted_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `app/views/mailers/notify_mailer/account_deleted_email.html.erb`
- `app/views/mailers/notify_mailer/account_deleted_email.text.erb`
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When a user's account is deleted, the system sends a transactional confirmation email to the address associated with that account. The email addresses the user by name, confirms that the account has been successfully deleted, provides the community's contact email for follow-up questions, and signs off with the community name. Both an HTML and a plain-text variant are rendered. The community name in the subject line and body is resolved per-subforem, so multi-tenant deployments each display their own community name.

## Design Intent

Sending a deletion confirmation closes the loop for the user: it provides proof of deletion and a contact path if the deletion was unintended or if the user has follow-up questions. Using I18n for the subject and a shared `contact_mailto_html` translation key keeps the wording consistent with other transactional emails and makes the text easy to localize.

## Key Members

- `params[:name]` — the display name of the deleted user, interpolated into the greeting
- `params[:email]` — the recipient address; the account's email at the time of deletion
- `@subforem_id` — optional subforem context used to resolve the correct community name
- `Settings::Community.community_name(subforem_id:)` — returns the community name for the subject line
- `ForemInstance.contact_email` — the platform contact address linked in the email body
- `community_name` (view helper) — resolves the community name inside the template

## Scenarios

### Standard account deletion confirmation

1. An account deletion is triggered for a user with a known name and email address.
2. The mailer is invoked with `params[:name]` set to the user's display name and `params[:email]` set to the user's email address.
3. The system resolves the community name from `Settings::Community.community_name` using the default subforem context.
4. The subject is set to `"<community name> - Account Deletion Confirmation"`.
5. The email is addressed to the user by name and states that the account has been successfully deleted.
6. The body includes the platform contact email as a mailto link (HTML) or plain text (text variant).
7. The email is signed off with "The <community name> Team".
8. The email is sent to the address supplied in `params[:email]`.

### Subforem-specific community name

1. An account deletion is triggered within a subforem that has its own community name configured.
2. The mailer is invoked with `@subforem_id` set to the relevant subforem's identifier.
3. The system resolves the community name for that subforem via `Settings::Community.community_name(subforem_id: @subforem_id)`.
4. Both the subject line and the email body display the subforem's community name rather than the default community name.

## Failures / Exceptions

- If `params[:name]` is nil or blank, the greeting renders without a name; no error is raised.
- If `params[:email]` is nil, the underlying mail library raises an addressing error; callers are responsible for providing a valid address.
