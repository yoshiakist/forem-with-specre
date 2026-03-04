---
id: "01KJVJ45XH7EQE2H412F1ZGN0V"
name: "user_completes_onboarding_checklist"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/onboardings_controller.rb`
- `app/javascript/onboarding/Onboarding.jsx`
- `app/javascript/onboarding/utilities.js`
- `app/javascript/onboarding/components/Navigation.jsx`
- `app/javascript/onboarding/components/EmailPreferencesForm.jsx`
- `app/javascript/onboarding/components/actions.js`
- `app/javascript/packs/Onboarding.jsx`
- `app/views/onboardings/show.html.erb` (Template)
- `app/views/onboardings/_newsletter.html.erb` (Template)
- `app/views/onboardings/_task_card.html.erb` (Template)
- `spec/requests/onboardings_spec.rb` (Test)
- `spec/system/onboardings/user_completes_onboarding_spec.rb` (Test)
- `app/javascript/onboarding/__tests__/Onboarding.test.jsx` (Test)
- `app/javascript/onboarding/components/__tests__/EmailPreferencesForm.test.jsx` (Test)

## Functional Overview

After registration, a new user is directed to `GET /onboarding`, which renders a full-screen slideshow powered by the `Onboarding` Preact component. The slideshow presents an ordered sequence of slides: profile form, then either follow-tags + follow-users (for regular users) or follow-subforems (for root-subforem users), then an optional custom CTA slide (controlled by the `onboarding_custom_cta_slide` feature flag), and finally an email preferences slide. The user navigates forward ("Continue" / "Finish") and backward via the `Navigation` component, which also renders a progress stepper. On the email preferences slide, the user can opt into the newsletter; if they click "Finish" without opting in, a reconsideration prompt appears offering "No thank you" or "Count me in". Email digest preferences are persisted via `PATCH /onboarding/notifications`. Completion is recorded by `PATCH /onboarding/checkbox`, which sets `saw_onboarding` to true and optionally records `checked_code_of_conduct` and `checked_terms_and_conditions`. After finishing, the user is redirected to the home feed (or to a recent billboard-interaction path if one exists in localStorage). Individual slides (profile form, follow tags, follow users, follow subforems) are covered by their own specre cards.

## Design Intent

The slideshow orchestrator (`Onboarding`) builds the slide list once at construction time based on the `isRootSubforem` flag read from the DOM, keeping slide ordering deterministic and easy to audit. The `Navigation` component is a pure presentational component shared by all slides, so progress-stepper and button-label logic (Continue / Skip for now / Finish) lives in one place. The email reconsideration prompt is implemented as an inline overlay rather than a separate route, so the user stays in the same slide context without a page reload.

## Scenarios

### Standard user navigates and completes the slideshow

1. Authenticated user visits `/onboarding`; the server renders the container with community config data attributes and loads the `Onboarding` JavaScript pack.
2. The `Onboarding` component initialises with the slide sequence: ProfileForm → FollowTags → FollowUsers → EmailPreferencesForm (plus optional CustomCta at index 3).
3. The user advances through each slide by clicking "Continue"; the `Navigation` stepper updates to reflect progress. Slides report their current page via `PATCH /onboarding` (`updateOnboarding`).
4. On the final (EmailPreferencesForm) slide, the user checks the newsletter checkbox and clicks "Finish". The component calls `PATCH /onboarding/notifications` with `email_newsletter: true`.
5. On success, `localStorage.shouldRedirectToOnboarding` is set to false and `nextSlide()` completes the flow, redirecting the user to the home feed (or a recent billboard path).

### User declines newsletter and is shown reconsideration prompt

1. On the EmailPreferencesForm slide, the user leaves the newsletter checkbox unchecked and clicks "Finish".
2. The component detects the unchecked state and sets `askingToReconsiderEmail: true`, rendering the reconsideration overlay.
3. If the user clicks "No thank you", `finishWithoutEmail` is called: `shouldRedirectToOnboarding` is cleared and `next()` proceeds without a notifications PATCH.
4. If the user clicks "Count me in", `finishWithEmail` is called: `PATCH /onboarding/notifications` is sent with both `email_newsletter: true` and `email_digest_periodic: true`, then `next()` proceeds.

### Root-subforem user follows a different slide sequence

1. When `document.body.dataset.isRootSubforem` is `'true'`, the `Onboarding` component builds the slide list as ProfileForm → FollowSubforems → EmailPreferencesForm (skipping FollowTags and FollowUsers).
2. Navigation and completion behave identically to the standard flow.

### User navigates backward through slides

1. On any slide other than the first, the user clicks the back button in the `Navigation` component.
2. `prevSlide()` decrements `currentSlide` and re-renders the previous slide within the same `FocusTrap`.
3. On the first slide, the back button is hidden (`hidePrev` prop) so backward navigation is not possible.

### Checkbox and ToS acceptance are recorded on completion

1. When the onboarding flow calls `PATCH /onboarding/checkbox` (from the profile form slide or a ToS slide), the `checkbox` action sets `saw_onboarding = true` on the current user and persists `checked_code_of_conduct` and `checked_terms_and_conditions` if provided.
2. A 200 response is returned on success; a 422 with error details is returned if the save fails.

## Failures / Exceptions

- `PATCH /onboarding` returns 422 with `{ errors: "..." }` if the username is blank or if `Users::Update` fails validation.
- `PATCH /onboarding/notifications` returns 422 with `{ errors: "..." }` if the notification settings save fails.
- `PATCH /onboarding/checkbox` returns 422 with error details if the user record cannot be saved.
- All endpoints require authentication; unauthenticated requests are redirected to `/magic_links/new`.
- If the `Onboarding` JavaScript pack fails to load, a console error is logged and the user remains on a blank container.
