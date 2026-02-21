---
id: "01KHZMED56WYNARJ0KFNWFZHZX"
name: "user_can_skip_poll_in_survey"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/poll_skips_controller.rb`
- `app/models/poll_skip.rb`
- `spec/requests/poll_skips_spec.rb` (Test)
- `spec/models/poll_skip_spec.rb` (Test)
- `spec/factories/poll_skips.rb` (Test)

## Functional Overview

An authenticated user may skip a poll within a survey, recording that they chose not to answer without casting a vote. When a skip is submitted, the system checks whether the survey allows further submission by the current user; if resubmission is not permitted, the request is silently acknowledged without creating a new record. For survey polls, a new `PollSkip` record is created carrying a `session_start` timestamp so that session-scoped uniqueness can be enforced. For regular (non-survey) polls the legacy idempotent `create_or_find_by` path is used instead. After a skip is persisted, `SurveyCompletionService` is called to check whether all polls in the survey have now been answered or skipped, potentially marking the survey as complete for that user.

## Design Intent

The `session_start` field allows a single survey to be presented across multiple sessions without conflating responses from different visits. The `one_vote_per_poll_per_user_per_session` validation ensures a user cannot skip the same poll twice in the same session, maintaining integrity of survey completion tracking. Using `save!` (raising on failure) rather than `save` delegates error recovery entirely to the `rescue StandardError` block, keeping the happy path concise while still reporting unexpected failures to Honeybadger.

## Key Members

- `session_start: Integer` — Unix-epoch integer identifying the survey session; defaults to `0` for requests that omit it. Used as part of the uniqueness scope by `PollSkip#one_vote_per_poll_per_user_per_session`.
- `POLL_SKIPS_PERMITTED_PARAMS` — strong-parameters allowlist: `[:poll_id, :session_start]`.
- `SurveyCompletionService.check_and_mark_completion` — called after every successful skip to determine whether the survey is now fully completed.

## Scenarios

### Successful skip of a survey poll

1. An authenticated user sends a POST request to `/poll_skips` with a valid `poll_id` and an optional `session_start` value.
2. The system looks up the poll and confirms the poll belongs to a survey and that the survey permits a new submission from this user.
3. A new `PollSkip` record is created linking the user, the poll, and the session identifier.
4. `SurveyCompletionService` evaluates whether all polls in the survey have been answered or skipped for this session.
5. The system responds with the poll's current voting data and `voted: false`, indicating no vote was cast.

### Skip silently ignored because resubmission is not allowed

1. An authenticated user sends a POST request to `/poll_skips` for a survey poll they have already interacted with in a session where resubmission is disabled.
2. The system looks up the poll, finds the poll's survey exists, and determines `can_user_submit?` returns false for the current user.
3. No new `PollSkip` record is created and `SurveyCompletionService` is not called.
4. The system responds immediately with the poll's current voting data and `voted: false`.

### Skip blocked by session-scoped uniqueness validation

1. An authenticated user attempts to skip the same survey poll a second time within the same session.
2. A new `PollSkip` is instantiated and `save!` is called.
3. The `one_vote_per_poll_per_user_per_session` validation detects that a vote or skip was already recorded for this user and session via `Poll#vote_previously_recorded_for_in_session?`, and adds a validation error.
4. `save!` raises an exception, which is caught by the `rescue StandardError` block.
5. The error is reported to Honeybadger with context including `user_id`, `poll_id`, and the action name.
6. The system responds with an empty voting data payload and `voted: false`.

### Successful skip of a regular (non-survey) poll

1. An authenticated user sends a POST request to `/poll_skips` with a `poll_id` for a poll that does not belong to any survey.
2. The system looks up the poll and determines no survey is associated.
3. The system uses idempotent `create_or_find_by` to record the skip, ensuring duplicate requests produce only one record.
4. `SurveyCompletionService` is called (no-op for non-survey polls).
5. The system responds with the poll's current voting data and `voted: false`.

## Failures / Exceptions

- If any `StandardError` is raised during skip creation (e.g., a validation failure via `save!`, or a database error), the exception is reported to Honeybadger with `user_id`, `poll_id`, and `action: "poll_skip_create"` as context. The response returns an empty voting distribution and `voted: false` so the client can handle the state gracefully without exposing internal errors.
- Unauthenticated requests to `POST /poll_skips` are rejected by the `before_action :authenticate_user!` filter before the action body is reached.
