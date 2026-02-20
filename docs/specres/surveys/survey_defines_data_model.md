---
id: "01KHYDGFH91Y4CKRSK7XB9CAY2"
name: "survey_defines_data_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/survey.rb
- spec/models/survey_spec.rb (Test)
- spec/factories/surveys.rb (Test)

## Functional Overview

The `Survey` model represents a survey containing multiple ordered polls. It manages the survey lifecycle including title validation, unique slug generation with backward-compatible slug rotation, user completion tracking across sessions, and resubmission eligibility. A survey is considered completed by a user only when all its polls have been responded to (voted, skipped, or text-responded) within the same session.

## Scenarios

### Slug generation on creation

1. When a survey is created with a title, the system auto-generates a slug from the parameterized title suffixed with a random hex token.
2. The slug is not regenerated when the title is updated afterward.
3. The slug can be manually overridden to a custom value.
4. The slug must be unique across all surveys, but nil is allowed.

### Slug rotation on update

1. When the slug is changed, the previous slug is stored in `old_slug` and any prior `old_slug` is moved to `old_old_slug`.
2. This rotation preserves up to two historical slugs for backward-compatible URL redirects.

### Completion check scoped to latest session

1. A survey with no polls is considered completed by any user.
2. A user who has not responded to any poll is not considered to have completed the survey.
3. A user who has responded to some but not all polls in the latest session is not considered to have completed the survey.
4. A user who has responded to all polls in the same session (via votes, skips, or text responses) is considered to have completed the survey.
5. Responses spread across different sessions do not count — only responses sharing the same `session_start` value as the latest session are considered.

### Submission eligibility

1. An anonymous (nil) user is always allowed to submit.
2. When `allow_resubmission` is enabled, any user is always allowed to submit regardless of prior completion.
3. When `allow_resubmission` is disabled, a user who has already completed the survey in the latest session is blocked from submitting again.

### Session management

1. The latest session number is the maximum `session_start` value across all of the user's poll votes, poll skips, and poll text responses for the survey's polls.
2. If the user has no responses, the latest session is 0.
3. Generating a new session returns the latest session number incremented by 1.

## Key Members

- `polls` — ordered association of `Poll` records (by position), with nested attributes and dependent nullification.
- `poll_votes` — through association to `PollVote` via polls.
- `survey_completions` — dependent-destroy association tracking which users have completed the survey.
- `allow_resubmission` — boolean flag controlling whether users can retake the survey.
- `old_slug`, `old_old_slug` — historical slugs for backward-compatible URL lookups.
