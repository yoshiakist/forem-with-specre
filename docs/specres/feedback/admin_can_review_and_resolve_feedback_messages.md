---
id: "01KJ25KAPB0FAFF74WX0TD106P"
name: "admin_can_review_and_resolve_feedback_messages"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/admin/feedback_messages_controller.rb`
- `app/helpers/feedback_messages_helper.rb`
- `app/javascript/admin/controllers/reaction_controller.js`
- `app/views/admin/feedback_messages/index.html.erb` (Template)
- `app/views/admin/feedback_messages/show.html.erb` (Template)
- `app/views/admin/feedback_messages/_feedback_message.html.erb` (Template)
- `app/views/admin/feedback_messages/_abuse_reports.html.erb` (Template)
- `app/views/admin/feedback_messages/_style.html.erb` (Template)
- `app/views/mailers/notify_mailer/feedback_message_resolution_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/feedback_message_resolution_email.text.erb` (Template)
- `app/views/mailers/notify_mailer/feedback_response_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/feedback_response_email.text.erb` (Template)
- `spec/requests/admin/feedback_messages_spec.rb` (Test)
- `spec/helpers/feedback_messages_helper_spec.rb` (Test)

## Functional Overview

Admins can view, filter, and triage user-submitted feedback messages (abuse reports and other reports) through a dedicated admin interface. The index lists reports filtered by status (`Open`, `Resolved`, or `Invalid`) and optionally by search criteria such as reported URL, reporter username, and category. Each report card shows reporter, offender, and reported content details, and provides controls to update the report status, send resolution emails to the reporter, offender, or affected party, and leave internal admin notes. Alongside reports, a panel of recent `vomit` flag reactions on users, articles, and comments is displayed and can be individually confirmed or invalidated. A detail view shows a single report with the same actions. The `FeedbackMessagesHelper` provides pre-populated, community-branded email subject and body defaults for each recipient role. When a note is saved, a Slack notification is dispatched via `Slack::Messengers::Note`.

## Design Intent

Reports with a `reported` subject whose score is at or below `-125` are excluded from the listing, preventing action on already-heavily-penalized content. The `vomit` reaction panel is scoped to the past two weeks and capped at 10 entries for `Resolved` and `Invalid` views to keep the panel manageable, while `Open` shows all recent flags with no limit. Ransack parameters are reconciled so that bookmarked or linked URLs using `q[status_eq]` or `q[category_eq]` are transparently mapped to the top-level `status` and `category` params used by the view.

## Key Members

- `SCORE_MIN` — threshold (`-125`) below which a reported subject is excluded from the listing
- `status` — report lifecycle value; one of `Open`, `Invalid`, or `Resolved`
- `feedback_type` / `category` — type of the report (e.g., `abuse-reports`), used when creating notes and filtering
- `ReactionController` Stimulus values: `id` (reaction ID), `url` (PATCH endpoint for updating the reaction status)

## Scenarios

### Browsing and filtering reports

1. An admin navigates to the reports index; the controller defaults the status filter to `Open`.
2. Ransack parameters are reconciled so that search params embedded in the URL are mapped to the correct filter fields.
3. The list of `FeedbackMessage` records is fetched with reporter, offender, affected, and reported associations eager-loaded, ordered newest first, and filtered to the selected status.
4. Records whose reported subject has a score at or below `-125` are removed from the result.
5. The page also loads associated email messages, admin notes, and a panel of recent `vomit` reactions scoped to the last two weeks.

### Resolving or invalidating a report

1. The admin clicks a status button ("Resolved" or "Invalid") on a report card.
2. The page posts the report ID and the chosen status to `save_status_admin_reports_path`.
3. The controller finds the `FeedbackMessage` by ID and attempts to update its `status` field.
4. On success, the response returns `{ outcome: "Success" }` and the UI collapses the report card and displays a confirmation message.
5. On failure, the response returns the model's validation error messages.

### Sending a resolution email to a report participant

1. The admin selects a recipient tab (Reporter, Offender, or Affected) within the email form on a report card.
2. The pre-populated subject and body are provided by `FeedbackMessagesHelper` methods (`reporter_email_details`, `offender_email_details`, `affected_email_details`), each returning community-branded text.
3. The admin optionally edits the subject and body, then clicks "Send Email".
4. The page posts the recipient address, subject, body, email type, and feedback message ID to `send_email_admin_reports_path`.
5. The controller calls `NotifyMailer.with(params).feedback_message_resolution_email.deliver_now`; on success it returns `{ outcome: "Success" }` and the UI shows a success notice, otherwise it returns `{ outcome: "Failure" }`.

### Adding an internal admin note

1. The admin types a note in the notes section of a report card and clicks "Submit Note".
2. The page posts the content, reason, noteable ID and type (`FeedbackMessage`), and author ID to `create_note_admin_reports_path`.
3. The controller creates a new `Note` record; on success it enriches the params with the author name and current report status, then calls `Slack::Messengers::Note.call` to send a Slack notification.
4. The response returns `{ outcome: "Success", content: ..., author_name: ... }` and the new note is appended to the notes list without a page reload.
5. On failure, the response returns the note's validation errors.

### Confirming or invalidating a vomit flag reaction

1. The admin sees the "Flag Reactions" panel listing recent `vomit` reactions on users, articles, and comments.
2. For user-type reactables, clicking "CONFIRM" triggers a browser confirmation dialog before proceeding; for other types it proceeds immediately.
3. The `ReactionController` Stimulus controller sends a PATCH request to the reaction's admin URL with the new status (`confirmed` or `invalid`).
4. On success, the reaction row and its separator are removed from the DOM; if the reactable type requires a full page reload (non-removable elements), the page reloads instead.
5. On failure, an alert is shown with the error message.

## Failures / Exceptions

- If `FeedbackMessage#update` fails in `save_status`, the JSON response contains the model's full error messages instead of `"Success"`.
- If `NotifyMailer` delivery fails in `send_email`, the response returns `{ outcome: "Failure" }`.
- If `Note#save` fails in `create_note`, the response returns the note's validation errors.
- If the recipient email address field is blank when submitting the email form, a client-side warning is shown and the request is not sent.
- Vomit reactions whose reactable has been deleted are excluded from the panel (`q.select(&:reactable)`).
