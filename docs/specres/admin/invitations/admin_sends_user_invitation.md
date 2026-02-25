---
id: "01KJ9FXHGQ9PCEYWSQY1713C0E"
name: "admin_sends_user_invitation"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/invitations_controller.rb`
- `app/views/admin/invitations/new.html.erb`
- `app/mailers/devise_mailer.rb`
- `app/views/devise/mailer/invitation_instructions.html.erb`
- `app/views/devise/mailer/invitation_instructions.text.erb`
- `spec/requests/admin/invitations_spec.rb` (Test)
- `spec/system/admin/admin_invites_user_spec.rb` (Test)
- `app/views/devise/invitations/edit.html.erb` (Template)
- `app/views/admin/users/new/show.html.erb` (Template)
- `app/views/admin/users/new/_tools_section_header.html.erb` (Template)

## Functional Overview

An admin can invite a new user to the Forem community by submitting the user's email address along with optional customizations for the invitation email (subject, message body, and footnote). The system checks that no already-registered user with that email exists, generates a provisional username, creates an unregistered user record via Devise's invitation mechanism, and enqueues a transactional email containing a tokenized acceptance link. When the invitation email is sent, the custom subject replaces the default "Invitation Instructions" subject, the custom message replaces the standard intro text, and the custom footnote is appended after the acceptance link. The invitation form is only shown when SMTP is configured; otherwise an SMTP setup notice is displayed instead.

## Design Intent

Customizable invitation fields (subject, message, footnote) allow admins to craft community-specific or context-specific onboarding messages without touching email templates. Separating the SMTP guard at the view layer keeps the controller logic clean and avoids sending invitations that could never be delivered.

## Key Members

- `email` — the invitee's email address; used for duplicate checking and user creation
- `custom_invite_subject` — replaces the default "Invitation Instructions" email subject
- `custom_invite_message` — replaces the default intro paragraph in the invitation email body (rendered as Markdown)
- `custom_invite_footnote` — appended after the acceptance link in the email body (rendered as Markdown)
- `registered: false` — flag set on the created user record to indicate they have not yet accepted the invitation

## Scenarios

### Admin views the invitation form when SMTP is enabled

1. Admin navigates to the new invitation page (`GET /admin/member_manager/invitations/new`).
2. Because SMTP is configured, the system displays the "Invite Users" form with fields for email, custom subject, custom message, and custom footnote.

### Admin views SMTP setup notice when SMTP is disabled

1. Admin navigates to the new invitation page.
2. Because SMTP is not configured, the system displays a notice directing the admin to configure SMTP settings; the invitation form is not shown.

### Admin sends a basic invitation

1. Admin submits the invitation form with a valid email address (and optionally leaves the custom fields blank).
2. System verifies that no already-registered user with that email exists.
3. System generates a provisional username derived from the email local part.
4. System creates an unregistered user record and enqueues an invitation email via Devise with the default subject "Invitation Instructions".
5. Admin is redirected to the invitations index with a success flash message.

### Admin sends a customized invitation

1. Admin submits the form with a valid email and fills in a custom subject, custom message, and custom footnote.
2. System creates the unregistered user and enqueues the invitation email, passing the custom fields to the mailer.
3. The sent email uses the custom subject, renders the custom message as Markdown in place of the standard intro, and appends the custom footnote after the acceptance link.

### System rejects invitation when user is already registered

1. Admin submits the invitation form with an email belonging to an already-registered user.
2. System detects the conflict without creating a new user or sending an email.
3. Admin is redirected to the invitations index with an error flash message indicating the duplicate email.

## Failures / Exceptions

- If a user with the submitted email already exists **and is registered**, the invitation is rejected, no user record is created or modified, and an error flash is displayed. Unregistered users (previously invited but not yet accepted) do not trigger this guard.
