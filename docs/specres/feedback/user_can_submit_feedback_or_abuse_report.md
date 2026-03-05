---
id: "01KJ25JM22F6QQ01PMJXGHZVQ5"
name: "user_can_submit_feedback_or_abuse_report"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/feedback_messages_controller.rb`
- `app/models/feedback_message.rb`
- `app/services/slack/messengers/feedback.rb`
- `app/views/feedback_messages/_form.html.erb` (Template)
- `app/views/feedback_messages/index.html.erb` (Template)
- `app/views/feedback_messages/new.html.erb` (Template)
- `spec/requests/feedback_messages_spec.rb` (Test)
- `spec/models/feedback_message_spec.rb` (Test)
- `spec/services/slack/messengers/feedback_spec.rb` (Test)
- `spec/system/feedback_message_spec.rb` (Test)

## Functional Overview

Users — both authenticated and anonymous — can submit a `FeedbackMessage` through a public form, choosing between an abuse report (`feedback_type: "abuse-reports"`) or general feedback. On submission, the controller validates reCAPTCHA (if enabled and the submitter does not qualify for bypass), enforces a rate limit, and persists the message. On success, a Slack notification is dispatched asynchronously via `Slack::Messengers::Feedback`, and authenticated users receive a one-time confirmation email (cached per user to avoid duplicate sends). On failure, the form is re-rendered with error details. For abuse reports, the model attempts to resolve the reported URL to a concrete entity (user, article, comment, or billboard) before saving.

## Design Intent

The CSRF check is skipped (`skip_before_action :verify_authenticity_token`) to allow the form to be embedded on the `/report-abuse` page and called from JSON clients without a session cookie. A cache key keyed to the user prevents multiple confirmation emails from being sent during the 24-hour window even if the user submits several reports.

## Key Members

- `feedback_type` — distinguishes abuse reports (`"abuse-reports"`) from other types (e.g., `"bug"`, `"other"`); drives conditional validations and the Slack channel target
- `category` — required for abuse reports; must be one of `FeedbackMessage::CATEGORIES`: `["spam", "other", "rude or vulgar", "harassment", "bug", "listings"]`
- `status` — lifecycle status of the record; one of `FeedbackMessage::STATUSES`: `["Open", "Invalid", "Resolved"]`
- `reported_url` — required for abuse reports; used to resolve the reported entity via URL pattern matching

## Scenarios

### Successful abuse report submission (anonymous user)

1. An anonymous visitor navigates to the report-abuse page and fills in the category, reported URL, and a message.
2. If reCAPTCHA is enabled, they complete the reCAPTCHA challenge; if not configured or the user qualifies for bypass, this step is skipped.
3. The system verifies reCAPTCHA and confirms the rate limit has not been reached.
4. The `FeedbackMessage` is saved; the `determine_reported_from_url` callback attempts to link the `reported_url` to a matching entity (user, article, comment, or billboard).
5. `Slack::Messengers::Feedback` enqueues an asynchronous Slack notification to the `"abuse-reports"` channel with a `:cry:` emoji and an "anonymous report" label.
6. The user is redirected to `feedback_messages_path`, which shows a confirmation message.

### Successful submission by an authenticated user

1. A signed-in user submits a valid feedback or abuse report form.
2. The controller attaches `reporter_id` from the current session, validates reCAPTCHA (bypassed for trusted or long-standing users), and checks the rate limit.
3. The `FeedbackMessage` is saved and a Slack notification is enqueued.
4. A confirmation email (`NotifyMailer#feedback_response_email`) is dispatched via a cache-guarded block so only one email is sent within a 24-hour window.
5. HTML requests are redirected to `feedback_messages_path`; JSON requests receive `{ success: true, message: "..." }`.

### reCAPTCHA failure

1. reCAPTCHA is enabled and the user submits the form without completing the challenge (or it fails verification).
2. The message is not saved and no Slack notification is enqueued.
3. HTML requests re-render `pages/report_abuse` with a flash notice listing the errors; JSON requests receive `{ success: false, message: "...", status: "bad_request" }`.

### Rate limit reached

1. A user has already submitted the maximum allowed number of feedback messages within the rate-limit window.
2. `rate_limit!(:feedback_message_creation)` raises a `StandardError`; the controller catches it and adds the error to the model.
3. The submission is rejected and the form is re-rendered with the rate-limit error message. JSON clients receive a `bad_request` status.

### URL entity resolution on abuse report save

1. When a `FeedbackMessage` with `feedback_type: "abuse-reports"` is saved and `reported_url` is present and points to the application's own domain, the `before_save` callback `determine_reported_from_url` runs.
2. The URL path is matched against known patterns: billboard admin paths, comment paths (`/username/comment/id_code`), article paths (`/username/slug`), and user profile paths (`/username`).
3. If a matching entity is found, `reported` is set to that entity; otherwise it remains `nil`. Errors during resolution are silently rescued.

## Failures / Exceptions

- Validation rejects an abuse report that is missing `category` or `reported_url`, or whose `message` exceeds 2,500 characters, or whose `reported_url` or `category` exceed 250 characters.
- A reporter cannot file a duplicate abuse report for the same `reported_url` and `feedback_type` combination (uniqueness validation on `reporter_id` scoped to `REPORTER_UNIQUENESS_SCOPE`); anonymous reports are exempt from this check.
- Any error raised during URL-to-entity resolution in `determine_reported_from_url` is silently rescued so it does not block the save.
