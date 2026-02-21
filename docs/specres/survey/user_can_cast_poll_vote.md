---
id: "01KHZMA857XQ0MP5F9S9D2ZYCX"
name: "user_can_cast_poll_vote"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/poll_votes_controller.rb`
- `app/models/poll.rb`
- `app/models/poll_vote.rb`
- `app/models/poll_option.rb`
- `spec/requests/poll_votes_spec.rb` (Test)
- `spec/requests/poll_votes_controller_spec.rb` (Test)
- `spec/models/poll_vote_spec.rb` (Test)
- `spec/models/poll_spec.rb` (Test)
- `spec/models/poll_option_spec.rb` (Test)
- `spec/factories/polls.rb` (Test)
- `spec/factories/poll_votes.rb` (Test)
- `spec/factories/poll_options.rb` (Test)

## Functional Overview

An authenticated user can cast a vote on a poll by selecting one of its options. The controller resolves the target poll through the chosen option, then applies one of two distinct voting strategies depending on whether the poll belongs to a survey or is a standalone article poll. For survey polls, a new `PollVote` record is always created and stamped with a `session_start` identifier, allowing the same user to vote in successive survey sessions; resubmission is gated by `Survey#can_user_submit?`. For regular (article-attached) polls, the system finds or initializes a single vote record per user per poll and updates it in place, enabling vote changes without accumulating duplicates. After every successful vote, `SurveyCompletionService.check_and_mark_completion` is called to detect whether the user has now answered all polls in a survey. The `GET /poll_votes/:id` endpoint returns current voting distribution and whether the requesting user has already voted or skipped, without requiring authentication.

## Design Intent

The two-path strategy (survey vs. regular poll) preserves backward-compatible behavior for article-embedded polls while enabling the session-based multi-submission model required by surveys. Using `session_start` as part of the uniqueness scope lets a survey be answered multiple times by the same user across different sessions without conflating the responses, while still enforcing that a user cannot vote for the same option twice within one session. Silently returning `voted: true` when resubmission is disallowed avoids exposing survey configuration details to the client.

## Key Members

- `session_start: Integer` — epoch timestamp (or 0) that groups votes belonging to the same survey completion session; scoped into uniqueness constraints for survey polls
- `Poll#voting_data` — returns `{ votes_count:, votes_distribution: [[option_id, count], ...] }` drawn from counter-cache columns
- `Poll#vote_previously_recorded_for?(user_id:)` — checks whether any vote or skip exists for a user on a regular poll
- `Poll#vote_previously_recorded_for_in_session?(user_id:, session_start:)` — same check scoped to a specific session
- `Poll#allows_multiple_votes?` — true for `multiple_choice`, `scale`, and `text_input` poll types
- `PollVote` uniqueness rules — for single-choice survey polls, one vote per `(user_id, poll_id, session_start)`; for survey polls generally, one vote per `(user_id, poll_option_id, session_start)`; for regular single-choice polls, one vote per `(user_id, poll_id)`

## Scenarios

### Viewing voting data for a poll

1. A client sends `GET /poll_votes/:poll_id` (authentication optional).
2. The system loads the poll and looks up any existing vote or skip for the current user.
3. The system responds with `voting_data` (total vote count and per-option distribution), `poll_id`, the user's previously selected `user_vote_poll_option_id`, and a boolean `voted` indicating whether the user has already voted or skipped.

### Casting a vote on a regular (article) poll

1. An authenticated user submits `POST /poll_votes` with `poll_vote[poll_option_id]`.
2. The system finds the poll through the chosen option and confirms the poll has no associated survey.
3. The system finds or initializes a single `PollVote` record scoped to the user and poll, sets its `poll_option_id` to the submitted value, and saves it. If a record already existed, the previous choice is overwritten.
4. Counter-cache columns on `PollOption` and `Poll` are updated via after-save callbacks.
5. `SurveyCompletionService.check_and_mark_completion` is called (no-op for non-survey polls).
6. The system responds with updated `voting_data`, `poll_id`, `user_vote_poll_option_id`, and `voted: true`.

### Casting a vote on a survey poll in a new session

1. An authenticated user submits `POST /poll_votes` with `poll_vote[poll_option_id]` and `poll_vote[session_start]` (a non-zero integer identifying the session).
2. The system determines the poll belongs to a survey and calls `Survey#can_user_submit?` for the current user; the check passes (either first submission or resubmission is allowed).
3. The system creates a new `PollVote` record with `user_id`, `poll_id`, `poll_option_id`, and the provided `session_start`. Previous votes from earlier sessions are preserved unchanged.
4. `SurveyCompletionService.check_and_mark_completion` is called to check whether this vote completes the survey for the current session.
5. The system responds with updated `voting_data`, `poll_id`, `user_vote_poll_option_id`, and `voted: true`.

### Re-voting in a subsequent survey session when resubmission is allowed

1. A user who has already completed a survey in session 1 starts a new session (session 2) and submits a vote.
2. Because `allow_resubmission` is true on the survey, `Survey#can_user_submit?` returns true.
3. A new `PollVote` is created for session 2 alongside the existing session 1 record; both are retained in the database.
4. The response returns the current aggregated `voting_data` reflecting all sessions combined.

### Attempt to vote when survey resubmission is not allowed

1. An authenticated user submits `POST /poll_votes` for a poll that belongs to a survey where resubmission is disabled and the user has already submitted.
2. `Survey#can_user_submit?` returns false.
3. The system immediately renders a response with the current `voting_data` and `voted: true` without creating any new record.

## Failures / Exceptions

- Any `StandardError` raised during vote creation (e.g., unexpected database error) is caught, reported to Honeybadger with `user_id`, `poll_option_id`, and `action: "poll_vote_create"` as context, and the response returns a zero-count fallback `voting_data` with `voted: true` to avoid surfacing errors to the client.
- `authenticate_user!` blocks unauthenticated requests to `POST /poll_votes` before the action runs; `GET /poll_votes/:id` has no authentication requirement.
- Duplicate vote attempts within the same session on a single-choice survey poll, or on the same option of a multi-choice survey poll, are rejected by model-level uniqueness validations before the record is saved.
