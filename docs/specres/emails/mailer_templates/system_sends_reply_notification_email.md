---
id: "01KJ72GNWTSM6SDVV7DR8NDRHY"
name: "system_sends_reply_notification_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb` (Related)
- `app/views/mailers/notify_mailer/new_reply_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/new_reply_email.text.erb` (Template)
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When a user receives a reply to one of their comments, the system sends a notification email to the parent comment's author. The email includes the replier's name, a sanitized and truncated excerpt of the reply, the title of the original content being discussed, and a direct link to view the reply. The email is only sent if the recipient has a valid email address, has not hit the rate limit for email notifications, and if the processed reply content is non-empty after sanitization and truncation.

## Design Intent

Reply notifications use `CommentEmailScrubber` to sanitize HTML before inclusion in the email body, preventing XSS while preserving safe formatting. Content is truncated to 500 characters so the email remains concise and encourages the recipient to click through. Rate limiting by recipient email address prevents notification flooding. An unsubscribe token is generated so users can opt out of comment notification emails without needing to log in. Errors are reported to Honeybadger rather than raised, so a malformed comment does not prevent other emails from being sent.

## Key Members

- `@comment` — the reply comment whose author triggered the notification
- `@truncated_comment` — sanitized HTML of the reply body, truncated to 500 characters with a word-boundary separator
- `@user` — the parent comment's author who is the email recipient
- `@unsubscribe` — a signed token scoped to `:email_comment_notifications` that allows one-click unsubscribe
- Subject format: `"<replier name> replied to your <parent type>"` — where parent type reflects whether the parent was a comment or article

## Scenarios

### Email is sent successfully

1. A new reply comment is created on a parent comment authored by a different user.
2. The system invokes `NotifyMailer` with the reply comment as a parameter.
3. The mailer fetches the parent comment's author as the recipient.
4. The reply's HTML is sanitized with `CommentEmailScrubber` and truncated to 500 characters.
5. The system checks that the recipient has an email address, that the address has not exceeded the notification rate limit, and that the truncated content is not blank.
6. An unsubscribe token scoped to `email_comment_notifications` is generated for the recipient.
7. The email is delivered with the subject `"<replier name> replied to your <parent type>"` and addressed to the parent author's email.
8. The HTML template shows the replier's name, the title of the original content, the truncated reply body, and a "View reply" button.
9. The plain-text template shows the replier's name, the full stripped reply text, and the direct comment URL.

### Email is suppressed — recipient has no email address

1. The mailer checks the parent comment author's email.
2. The email address is blank.
3. The mailer returns early without sending any email.

### Email is suppressed — recipient has exceeded the notification rate limit

1. The mailer resolves the recipient's email address.
2. `RateLimitChecker` reports that the address has already received too many notification emails within the current window.
3. The mailer returns early without sending any email.

### Email is suppressed — reply content is blank after sanitization

1. The reply's HTML is sanitized and truncated.
2. The resulting truncated content is blank (e.g., the comment contained only disallowed tags).
3. The mailer returns early without sending any email.

## Failures / Exceptions

- Any `StandardError` raised during email preparation is rescued and reported to Honeybadger; the mailer returns without sending rather than propagating the exception.
- If the comment's commentable has been deleted, the HTML template falls back to displaying `"Content No Longer Available"` as the content title.
