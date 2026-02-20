---
id: "01KHYDHRP7XCMAJFEZ27YPZK5Y"
name: "survey_completion_tracks_user_progress"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/survey_completion.rb
- app/services/survey_completion_service.rb
- spec/models/survey_completion_spec.rb (Test)
- spec/factories/survey_completions.rb (Test)

## Functional Overview

The `SurveyCompletion` model and `SurveyCompletionService` together track which users have completed which surveys. The model enforces a one-completion-per-user-per-survey uniqueness constraint and provides query methods for checking completion status across multiple surveys. The service acts as a bridge between poll submissions and survey completions — after each poll response, it checks whether the user has now answered all polls in the survey and, if so, creates a completion record.

## Scenarios

### Recording a completion

1. Calling `mark_completed!` with a user and survey creates a new `SurveyCompletion` record with `completed_at` set to the current time.
2. Calling `mark_completed!` a second time for the same user-survey pair does not create a duplicate record; it returns the existing one.
3. A user can only have one completion record per survey (uniqueness on `user_id` scoped to `survey_id`).
4. The `completed_at` timestamp is required.

### Querying completion status

1. `user_completed_any?` returns true if the user has a completion record for at least one of the given survey IDs.
2. `user_completed_any?` returns false if the user has no completion records for any of the given survey IDs.
3. `user_completed_any?` returns false when user is nil or survey IDs list is empty.
4. `completed_survey_ids_for_user` returns all survey IDs the user has completed.
5. `completed_survey_ids_for_user` returns an empty array when user is nil or has no completions.

### Auto-completion after poll submission

1. When `SurveyCompletionService.check_and_mark_completion` is called with a user and a poll, the service checks whether the poll belongs to a survey.
2. If the poll has no survey, or the user is nil, the service does nothing.
3. If the survey is now completed by the user (all polls answered in the latest session), and no completion record exists yet, the service creates one.
4. If a completion record already exists, the service does not create a duplicate.

## Design Intent

The completion record is separated from the per-poll response tracking to provide a single, queryable flag for "this user finished this survey." This enables efficient lookups for features like billboard survey exclusion and email eligibility filtering without re-computing completion from individual poll responses each time.
