---
id: "01KJ75DN218QHHZ575VBJ95H29"
name: "admin_can_send_direct_email_to_user"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/users_controller.rb` (send_email action)
- `app/mailers/notify_mailer.rb` (user_contact_email method)
- `app/views/admin/users/show/emails/_form.html.erb` (Template)
- `app/views/mailers/notify_mailer/user_contact_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/user_contact_email.text.erb` (Template)
- `spec/requests/admin/users_spec.rb` (Test)
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

An admin can send a one-off direct email to a specific user from the admin user management page. The admin fills in a subject and body via a form, and the system sends the email immediately using `NotifyMailer#user_contact_email`. The action supports both browser (HTML) and AJAX (JSON) response formats, providing appropriate success or failure feedback in each case.

## Key Members

- `Admin::UsersController#send_email` — Controller action that receives email subject and body, dispatches via `NotifyMailer`.
- `NotifyMailer#user_contact_email` — Mailer method that looks up the user and sends the email with the provided subject and body.
- `EMAIL_ALLOWED_PARAMS` — Permitted parameters: `email_subject`, `email_body`.

## Scenarios

### Admin sends a direct email to a user via browser

1. Admin navigates to the user's admin page and fills in the email subject and body fields.
2. Admin submits the form.
3. System sends the email via `NotifyMailer#user_contact_email` to the user's email address.
4. Admin is redirected back with a success flash message.

### Admin sends a direct email to a user via AJAX

1. Admin submits the email form via an AJAX request.
2. System sends the email immediately.
3. System returns a JSON response with a success message and HTTP 200 status.

### Email delivery fails

1. Admin submits the email form.
2. `NotifyMailer` delivery returns a falsy result.
3. System displays a failure message — via flash redirect (browser) or JSON error with HTTP 503 status (AJAX).

## Failures / Exceptions

- If required parameters (`email_subject`, `email_body`) are missing, the system rescues `ActionController::ParameterMissing` and responds with a JSON error and HTTP 422 status.
- If the target user does not exist, the system raises `ActiveRecord::RecordNotFound`.
