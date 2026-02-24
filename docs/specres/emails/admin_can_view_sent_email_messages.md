---
id: "01KJ758NKFTEQKYMBYPEGR3817"
name: "admin_can_view_sent_email_messages"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/email_messages_controller.rb`
- `app/models/email_message.rb`
- `app/views/admin/email_messages/show.html.erb` (Template)
- `app/views/admin/users/show/emails/_index.html.erb` (Template)
- `spec/models/email_message_spec.rb` (Test)
- `spec/factories/email_messages.rb` (Test)

## Functional Overview

Admins can view the complete delivery history of sent email messages for any user. A dedicated admin page lists up to 50 of the most recently sent emails for a given user, each linking to a detail view. The detail view displays the message's subject, recipient address, sent timestamp, associated UTM campaign, mailer class, any linked abuse report (feedback message), and a rendered preview of the HTML email body. The `EmailMessage` model extends `Ahoy::Message`, adding a helper that extracts only the `<html>...</html>` portion of the stored content for safe rendering.

## Design Intent

Email message records are retained indefinitely when they are tied to a feedback message (i.e., emails manually sent by human admins), because those records may be needed as evidence in abuse investigations. Automated delivery records without a feedback message association are periodically bulk-deleted to keep the table manageable. The `html_content` helper guards against partially structured or plain-text content by falling back gracefully when no `<html>` tag is present.

## Key Members

- `@user` — the `User` record whose email history is being viewed, resolved from `params[:user_id]`
- `@email` — the specific `EmailMessage` record, resolved from `params[:id]`
- `html_content` — instance method on `EmailMessage` that returns the `<html>…</html>` slice of the stored content, or the full content when no HTML wrapper is present, or an empty string when content is nil

## Scenarios

### Admin views the email delivery list for a user

1. Admin navigates to the user's admin profile page.
2. The emails panel queries up to 50 of the user's email messages ordered by `sent_at` descending.
3. Each email is displayed as a linked list item showing the subject and formatted sent date.
4. If the user has no email messages, a message indicates that no emails have been sent to that address.

### Admin opens the detail view for a specific email

1. Admin clicks the subject link in the email delivery list.
2. The controller looks up the user by `user_id` and the email record by `id` from the URL parameters.
3. The detail page displays subject, recipient address, sent date, UTM campaign, mailer name, and a link to the associated abuse report when a feedback message is present.
4. The rendered HTML content of the email body is shown in a sandboxed preview area.

### Email body contains a full HTML document

1. The stored content includes a `<html>...</html>` wrapper.
2. `html_content` extracts and returns only the slice from `<html` to `</html>`.
3. The admin sees a clean rendered preview of the email body without surrounding storage artifacts.

### Email body contains plain text or partial content

1. The stored content has no `<html>` tag.
2. `html_content` returns the full content string as-is.
3. The admin sees the raw text in the preview area.

### Email body content is nil

1. The `content` field is `nil` (e.g., delivery record was partially written).
2. `html_content` returns an empty string.
3. The preview area renders as blank without raising an error.

## Failures / Exceptions

- When `content` is `nil`, `html_content` returns `""` rather than raising a `NoMethodError`, ensuring the show view renders safely.
