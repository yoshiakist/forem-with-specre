---
id: "01KHZKDENF1FEDNJQD6XXKWAKZ"
name: "user_can_vote_on_survey_polls"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/surveys_controller.rb`
- `app/models/survey.rb`
- `app/models/survey_completion.rb`
- `app/services/survey_completion_service.rb`
- `spec/controllers/surveys_controller_spec.rb` (Test)
- `spec/requests/surveys_controller_spec.rb` (Test)
- `spec/models/survey_spec.rb` (Test)
- `spec/models/survey_completion_spec.rb` (Test)
- `spec/factories/surveys.rb` (Test)
- `spec/factories/survey_completions.rb` (Test)

## Functional Overview

Authenticated users can retrieve their current voting state for a survey via `GET /surveys/:id/votes`. The endpoint returns the user's existing responses (poll votes and text responses keyed by poll ID), whether they are eligible to submit, whether they have already completed the survey, and session information. A survey tracks responses in numbered sessions; a user's completion is determined by whether they have responded to every poll in their latest session (via vote, skip, or text response). If the survey allows resubmission and the user has already completed it, the endpoint generates a new session number and returns an empty votes map so the frontend presents a clean slate. When resubmission is not allowed and the user has already completed the survey, submission eligibility is denied and the existing responses are returned. `SurveyCompletionService` is called after each poll interaction to automatically mark the parent survey as completed once all polls are answered in a session, using `SurveyCompletion` to record the event idempotently.

## Design Intent

Session numbers allow multiple submission attempts to coexist in the database without overwriting prior answers. The session is an integer that increments by one each time a completed user starts a new round, keeping historical responses intact and enabling per-session aggregation. Completion is checked lazily (by counting responses in the latest session) rather than stored state, so the completion record (`SurveyCompletion`) is only written once via `find_or_create_by` to prevent duplicates.

## Key Members

- `session_start` — integer stamped on each `PollVote`, `PollSkip`, and `PollTextResponse` record, scoping responses to a single attempt
- `allow_resubmission` — boolean flag on `Survey` controlling whether a completed user can submit again
- `current_session` — the highest `session_start` found across the user's responses for this survey (0 when none exist)
- `new_session` — `current_session + 1`, generated only when the user is eligible for a fresh attempt; `nil` otherwise

## Scenarios

### Unauthenticated user requests vote state

1. A visitor (not signed in) sends `GET /surveys/:id/votes`.
2. The `authenticate_user!` before-action intercepts the request and redirects to the sign-in page with HTTP 302.

### Authenticated user has not yet answered any polls

1. A signed-in user sends `GET /surveys/:id/votes` for a survey they have no responses for.
2. The system resolves the latest session as 0 (no prior activity).
3. `completed_by_user?` returns false; `can_user_submit?` returns true.
4. The endpoint responds with an empty votes map, `can_submit: true`, `completed: false`, `current_session: 0`, and `new_session: null`.

### Authenticated user has completed the survey and resubmission is not allowed

1. A signed-in user sends `GET /surveys/:id/votes` after answering every poll in session 1.
2. `completed_by_user?` returns true; `can_user_submit?` returns false because `allow_resubmission` is false.
3. Existing responses from session 1 are returned in the votes map, keyed by poll ID.
4. The endpoint responds with `can_submit: false`, `completed: true`, `allow_resubmission: false`, and `new_session: null`.

### Authenticated user has completed the survey and resubmission is allowed

1. A signed-in user sends `GET /surveys/:id/votes` after completing the survey when `allow_resubmission` is true.
2. `completed_by_user?` returns true; `can_user_submit?` returns true.
3. The system generates `new_session` as `current_session + 1` and uses it to scope the votes query — since no responses exist for that session yet, the votes map is empty.
4. The endpoint responds with `can_submit: true`, `completed: true`, `allow_resubmission: true`, the original session as `current_session`, and the new session number as `new_session`.

### Survey is automatically marked complete after all polls are answered

1. A user submits a vote or text response that brings their total responses in the current session up to the number of polls in the survey.
2. `SurveyCompletionService.check_and_mark_completion` is invoked with the user and the poll that was just answered.
3. `completed_by_user?` returns true, and because no `SurveyCompletion` record exists yet for this user and survey, `SurveyCompletion.mark_completed!` creates one with `completed_at` set to the current time.
4. Subsequent calls with the same user and survey do not create duplicate records.

## Failures / Exceptions

- If the survey ID does not exist, `Survey.find` raises `ActiveRecord::RecordNotFound`, which is rescued by a controller-level handler that renders the public 404 page with HTTP status 404.
- `SurveyCompletion` enforces uniqueness of `(user_id, survey_id)` at the database level; `mark_completed!` uses `find_or_create_by` to safely handle concurrent or repeated calls without raising a duplicate error.
