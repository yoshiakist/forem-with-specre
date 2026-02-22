---
id: "01KJ2HPF2KC2HBFRV0NS32DFR7"
name: "billboard_excludes_survey_completers"
status: "draft"
---

## Related Files

- `app/models/billboard.rb`
- `app/models/survey_completion.rb`
- `app/queries/billboards/filtered_ads_query.rb`
- `spec/integration/billboard_survey_exclusion_integration_spec.rb` (Test)
- `spec/models/billboard_survey_exclusion_spec.rb` (Test)

## Functional Overview

Billboards (display ads) can be configured to exclude users who have completed specific surveys. When a billboard has `exclude_survey_completions` enabled and `exclude_survey_ids` populated, the ad selection pipeline filters it out for any signed-in user who has a `SurveyCompletion` record matching any of the listed survey IDs. The filtering is applied in `Billboards::FilteredAdsQuery#survey_completion_filtered_ads`, which splits the candidate billboards into two groups: those without survey exclusion (always eligible) and those with exclusion enabled (checked against the user's completion history using PostgreSQL array overlap). An instance-level convenience method `Billboard#exclude_user_due_to_survey_completion?(user)` provides the same check for single-billboard evaluation.

## Design Intent

The two-column approach (`exclude_survey_completions` boolean + `exclude_survey_ids` integer array) allows the exclusion feature to be toggled independently of the survey ID list, and the GIN index on the array column enables efficient overlap queries at scale. The query-level filtering in `FilteredAdsQuery` ensures excluded billboards never enter the selection pool, rather than being selected and then discarded, keeping impression counts accurate. A feature flag (`SKIP_SURVEY_COMPLETION_FILTERING`) allows operators to disable the filtering entirely without a code deploy.

## Key Members

- `Billboard#exclude_survey_completions` — boolean flag enabling survey-based exclusion for this billboard
- `Billboard#exclude_survey_ids` — integer array of survey IDs whose completers should not see this billboard
- `Billboard#exclude_user_due_to_survey_completion?(user)` — returns true if the user has completed any of the listed surveys; returns false if the feature is disabled, user is nil, or the list is empty
- `SurveyCompletion.user_completed_any?(user_id:, survey_ids:)` — class method that checks for the existence of any completion record matching the given user and survey IDs
- `Billboards::FilteredAdsQuery#survey_completion_filtered_ads` — splits billboard candidates and applies the PostgreSQL array overlap (`&&`) filter for the current user's completed survey IDs

## Scenarios

### Billboard excluded for a user who completed a listed survey

1. A billboard is configured with `exclude_survey_completions: true` and `exclude_survey_ids: [3, 7]`.
2. A signed-in user who has a `SurveyCompletion` record for survey 3 requests a page.
3. `FilteredAdsQuery` queries `SurveyCompletion` for the user's completed survey IDs and finds `[3]`.
4. The overlap check (`exclude_survey_ids && ARRAY[3]`) is true; the billboard is excluded from the candidate pool.
5. The user does not see the billboard.

### Billboard shown to a user who has not completed any listed survey

1. Same billboard configuration as above.
2. A signed-in user has no `SurveyCompletion` records or only has completions for surveys not in the exclusion list.
3. The overlap check returns false; the billboard remains in the candidate pool and may be displayed.

### Billboard shown when exclusion is disabled

1. A billboard has `exclude_survey_completions: false` (regardless of `exclude_survey_ids` content).
2. The billboard is placed in the "no exclusion" group and is always eligible, even for users who have completed listed surveys.

### Billboard shown to anonymous users

1. A visitor who is not signed in requests a page.
2. `FilteredAdsQuery` skips the survey completion check entirely for nil users.
3. All billboards with survey exclusion enabled are included in the candidate pool.

### Feature flag disables filtering

1. The environment variable `SKIP_SURVEY_COMPLETION_FILTERING` is set to `"yes"`.
2. `FilteredAdsQuery` skips the survey completion filtering step entirely.
3. All billboards are eligible regardless of survey completion status.

## Failures / Exceptions

- If `exclude_survey_ids` contains a survey ID that does not correspond to an existing survey, no error is raised; `SurveyCompletion` simply finds no matching records and the billboard is shown.
- The `user_completed_any?` query uses an existence check (`EXISTS`), so performance is bounded regardless of the total number of completion records.
