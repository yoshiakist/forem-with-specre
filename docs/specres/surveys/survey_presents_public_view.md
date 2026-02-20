---
id: "01KHYDKBE1NWA0CH3ZQ7XR3RKG"
name: "survey_presents_public_view"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/surveys_controller.rb
- app/views/surveys/show.html.erb (Template)
- spec/controllers/surveys_controller_spec.rb (Test)
- spec/requests/surveys_controller_spec.rb (Test)
- spec/requests/surveys_spec.rb (Test)

## Functional Overview

`SurveysController` serves the public-facing survey experience. The `show` action renders a survey page by slug lookup with backward-compatible redirects for historical slugs. The `votes` JSON endpoint returns the authenticated user's existing responses, session state, and submission eligibility so the client-side JavaScript can hydrate the survey UI.

## Scenarios

### Show page with slug resolution

1. A request with the current slug renders the survey show page with polls ordered by position.
2. A request with a previous slug (`old_slug` or `old_old_slug`) results in a 301 permanent redirect to the current slug.
3. A request with an unknown slug returns a 404 Not Found response.
4. A request for an inactive survey returns a 404 Not Found response even if the slug is valid.

### Votes endpoint requires authentication

1. An unauthenticated request to the votes endpoint is rejected (redirect to sign-in).
2. An authenticated request returns a JSON payload containing `votes`, `can_submit`, `completed`, `allow_resubmission`, `current_session`, and `new_session`.

### Votes response for incomplete survey

1. When the user has not responded to any polls, `votes` is empty, `can_submit` is true, `completed` is false, and `current_session` is 0.
2. Only votes for polls belonging to the requested survey are included; votes for other polls are excluded.

### Votes response for completed survey without resubmission

1. When the user has completed the survey and `allow_resubmission` is false, the response includes the user's existing votes from the latest session, `can_submit` is false, `completed` is true, and `new_session` is null.

### Votes response for completed survey with resubmission

1. When the user has completed the survey and `allow_resubmission` is true, the response returns empty votes (fresh start for a new session), `can_submit` is true, `completed` is true, and `new_session` contains the next session number.

### Text input polls in votes

1. Text responses from text-input polls are included in the `votes` hash alongside option-based votes, keyed by poll ID with the text content as the value.
