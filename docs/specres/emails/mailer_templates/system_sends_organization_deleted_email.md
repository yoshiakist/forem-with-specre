---
id: "01KJ72SKJ1NPDRXKSKA8R47C82"
name: "system_sends_organization_deleted_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `app/views/mailers/notify_mailer/organization_deleted_email.html.erb`
- `app/views/mailers/notify_mailer/organization_deleted_email.text.erb`
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When an organization is deleted from the community, the system sends a confirmation email to the user who owned the organization. The email informs the recipient that the named organization has been successfully deleted from the platform, and includes a reference to the community contact email for follow-up. Both an HTML and a plain-text version of the message are rendered. The subject line is localized and incorporates the community name.

## Key Members

- `params[:name]` — The display name of the recipient (user)
- `params[:email]` — The delivery address of the recipient
- `params[:org_name]` — The name of the organization that was deleted
- `@subforem_id` — Used to resolve the community name for the subject line via `Settings::Community.community_name`
- `ForemInstance.contact_email` — The community contact email address included in the message body

## Scenarios

### Organization deletion confirmation is delivered

1. An organization is deleted by a user or admin action.
2. The caller invokes `NotifyMailer` with the recipient's name, email address, and the deleted organization's name as parameters.
3. The mailer sets the subject to "<community name> - Organization Deletion Confirmation", where the community name is resolved using the subforem context.
4. The email is addressed to the recipient's email address.
5. Both the HTML and plain-text parts greet the recipient by name, confirm that the named organization on the community has been successfully deleted, and include the community contact email.
6. The message is signed off by "The <community name> Team".

## Failures / Exceptions

- If `params[:email]` is absent or invalid, delivery will fail at the mail transport layer; the mailer itself performs no validation.
- If `ForemInstance.contact_email` is not configured, the contact link in the body will be blank or missing, but the email is still sent.
