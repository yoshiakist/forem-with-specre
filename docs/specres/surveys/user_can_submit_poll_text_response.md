---
id: "01KHZMEWNFHQAJSG7XYVQXEDTE"
name: "user_can_submit_poll_text_response"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/poll_text_responses_controller.rb`
- `app/models/poll_text_response.rb`
- `spec/requests/poll_text_responses_spec.rb` (Test)
- `spec/requests/poll_text_responses_controller_spec.rb` (Test)
- `spec/models/poll_text_response_spec.rb` (Test)
- `spec/factories/poll_text_responses.rb` (Test)

## Functional Overview

An authenticated user can submit a free-text response to a poll by posting to `POST /polls/:poll_id/poll_text_responses`. The controller verifies authentication, resolves the target poll, and — if the poll belongs to a survey that disallows further submissions for the current user — silently skips persistence and returns a success response anyway. Otherwise it creates a new `PollTextResponse` record scoped to the current user, the poll, and a `session_start` timestamp. On a successful save it delegates to `SurveyCompletionService` to detect whether the survey is now complete. Validation failures and unexpected exceptions are reported to Honeybadger but are never surfaced to the client; the response is always `{ success: true }`.

## Design Intent

The always-success response contract (`{ success: true }` regardless of outcome) is intentional: it prevents client-side polling loops and avoids revealing survey state or internal errors to the submitter. Errors are sent to Honeybadger for operator visibility without disrupting the user experience.

The uniqueness constraint on `(poll_id, user_id, session_start)` allows a user to answer the same poll multiple times across different survey sessions while still preventing exact duplicate submissions within a single session.

## Key Members

- `text_content` — the free-text answer; must be present and at most 1000 characters
- `session_start` — integer identifying the survey session; defaults to `0` when not provided; used as part of the uniqueness scope
- `poll_id / user_id` — associations required on every record; enforce ownership
- `SurveyCompletionService.check_and_mark_completion` — called after a successful save to determine whether the containing survey is now fully answered

## Scenarios

### Submit a new text response

1. An authenticated user sends a POST request to `/polls/:poll_id/poll_text_responses` with a non-empty `text_content` (≤ 1000 characters) and an optional `session_start` value.
2. The system looks up the poll by `poll_id`.
3. If the poll belongs to a survey, the system checks whether the user is still permitted to submit (via `Survey#can_user_submit?`). Because the survey allows submission, the check passes.
4. The system creates a new `PollTextResponse` record linked to the user, the poll, the provided text, and the session identifier.
5. After saving, the system calls `SurveyCompletionService` to evaluate whether the survey is now complete.
6. The system returns `{ success: true, message: "Text response submitted successfully" }` with HTTP 200.

### Submit a second response in a new survey session (resubmission)

1. An authenticated user who has already answered this poll in a previous session sends a POST request with a new `session_start` value that differs from all prior sessions.
2. The system finds the poll, confirms the survey allows resubmission, and verifies the uniqueness constraint is not violated (different `session_start`).
3. A new `PollTextResponse` record is created for the new session; the original record is unchanged.
4. `SurveyCompletionService` is invoked and the system returns `{ success: true }`.

### Survey resubmission is blocked

1. An authenticated user who has already completed a survey (where `allow_resubmission` is false) sends a POST request for a poll that belongs to that survey.
2. The system finds the poll, evaluates `Survey#can_user_submit?`, and determines the user is not permitted to submit again.
3. No `PollTextResponse` record is created.
4. The system returns `{ success: true, message: "Text response submitted successfully" }` immediately, without error.

### Validation failure (empty or oversized text)

1. An authenticated user sends a POST request with `text_content` that is either blank or exceeds 1000 characters.
2. The system attempts to build and save the `PollTextResponse` record.
3. Model validation fails; the record is not persisted.
4. The failure is reported to Honeybadger with the user id, poll id, and validation error messages.
5. The system still returns `{ success: true, message: "Text response submitted successfully" }` — the client receives no indication of the failure.

## Failures / Exceptions

- **Validation failure** — empty `text_content` or content exceeding 1000 characters causes the save to fail silently; Honeybadger receives the error details.
- **Duplicate submission in the same session** — the uniqueness constraint on `(poll_id, user_id, session_start)` prevents a second record; the save fails silently in the same way as a validation failure.
- **Unexpected exception** — any `StandardError` raised during the action is rescued, reported to Honeybadger, and masked behind the same `{ success: true }` response.
- **Unauthenticated request** — `before_action :authenticate_user!` redirects the request to `/magic_links/new` before the action body executes.
