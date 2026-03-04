---
id: "01KJVJ3JCADV1ASZQEPK5YT9RC"
name: "user_can_follow_custom_initiatives_during_onboarding"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/onboardings_controller.rb`
- `app/javascript/onboarding/components/CustomCta.jsx`
- `spec/requests/onboardings_spec.rb` (Test)

## Functional Overview

When the `onboarding_custom_actions` feature flag is enabled, an additional "Special Initiatives" slide is injected into the onboarding slideshow. The slide presents three pre-checked options: follow DEV Challenges (`devchallenge` tag), follow DEV Education Tracks (`deved` tag), and follow the Google AI organization account (`googleai`). The user may uncheck any option before proceeding. On completion, the `CustomCta` component submits the current checkbox state to `PATCH /onboarding/custom_actions`, which creates the appropriate follow relationships for each enabled option.

## Design Intent

The endpoint and slide are explicitly noted as hardcoded DEV-specific custom actions activated only when the `onboarding_custom_actions` feature flag is on. This allows the platform to gate the feature for gradual rollout without affecting the standard onboarding flow for other communities.

## Scenarios

### User accepts all three default initiatives

1. The `onboarding_custom_actions` feature flag is enabled and the user reaches the "Special Initiatives" slide during onboarding.
2. All three checkboxes — Follow DEV Challenges, Follow DEV Education Tracks, and Follow the Google AI Org Account — are pre-checked.
3. The user clicks the "Next" button without changing any selection.
4. The client sends `PATCH /onboarding/custom_actions` with `follow_challenges: true`, `follow_education_tracks: true`, and `follow_featured_accounts: true`.
5. The server looks up the `devchallenge` tag, the `deved` tag, and the `googleai` organization, and creates a follow relationship for each with the current user.
6. The server responds with HTTP 200 and the slideshow advances to the next slide.

### User opts out of one or more initiatives

1. The user reaches the "Special Initiatives" slide with all checkboxes pre-checked.
2. The user unchecks one or more checkboxes (e.g., unchecks "Follow DEV Education Tracks").
3. The client sends `PATCH /onboarding/custom_actions` with the unchecked options set to `false`.
4. The server only creates follow relationships for the options whose value is truthy; unchecked options are skipped entirely.
5. The server responds with HTTP 200.

### User unchecks all options

1. The user unchecks all three checkboxes on the "Special Initiatives" slide.
2. The client sends `PATCH /onboarding/custom_actions` with all three params set to `false`.
3. The server performs no follow operations and responds with HTTP 200.

### Referenced tag or organization does not exist

1. The server receives a truthy param (e.g., `follow_challenges: true`) but the corresponding tag (`devchallenge`) or organization (`googleai`) is not found in the database.
2. The follow operation is silently skipped for the missing record.
3. The other requested follow operations, if any, still proceed normally.
4. The server responds with HTTP 200.

## Failures / Exceptions

- If the tag or organization referenced by a param does not exist in the database, the follow for that item is silently skipped; no error is raised or returned to the client.
- Network errors during the client-side `fetch` call are caught and logged via `console.error`, and the slideshow advances to the next step regardless.
- Unauthenticated requests to `PATCH /onboarding/custom_actions` are rejected before reaching the action, redirecting the user to the sign-in flow.
