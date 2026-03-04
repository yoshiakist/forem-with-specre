---
id: "01KJVJ0PM6MVDTBJ7MH5JY9R5J"
name: "system_redirects_new_user_to_onboarding"
status: "draft"
---

## Related Files

- `app/javascript/packs/onboardingRedirectCheck.jsx`
- `spec/system/onboardings/user_completes_onboarding_spec.rb` (Test)

## Functional Overview

On every page load, the client-side onboarding redirect check runs after the DOM is ready and user data has been fetched. It examines whether the current user has completed onboarding — specifically whether `saw_onboarding`, `checked_code_of_conduct`, and `checked_terms_and_conditions` are all true. If the user has not completed onboarding and is not already on an excluded page (`/onboarding`, `/signout_confirm`, `/privacy`, `/admin/creator_settings/new`), the browser is redirected to `/onboarding` with a `referrer` query parameter. For creator users who have not yet seen onboarding, the system instead redirects to the creator settings wizard (`/admin/creator_settings/new`), excluding additional pages (`/code-of-conduct`, `/terms`) from triggering that redirect. On InstantClick-powered page transitions, the same check re-runs using the `shouldRedirectToOnboarding` key from `localStorage` to gate the redirect.

## Design Intent

The redirect check runs entirely client-side so that it can rely on the already-fetched user session data without requiring an additional server round-trip. Using `window.InstantClick.on('change', ...)` ensures the check fires on soft navigations as well as hard page loads, keeping the gate consistent across Forem's hybrid rendering model. The `shouldRedirectToOnboarding` localStorage flag allows the onboarding flow itself to suppress the redirect once the user has actively engaged with the wizard, preventing redirect loops.

## Key Members

- `saw_onboarding` — boolean on `currentUser`; true once the user has viewed the onboarding flow
- `checked_code_of_conduct` — boolean on `currentUser`; true once the user has accepted the code of conduct
- `checked_terms_and_conditions` — boolean on `currentUser`; true once the user has accepted the terms
- `shouldRedirectToOnboarding` — localStorage key (string `"true"` / `"false"` / absent); controls whether InstantClick transitions trigger a redirect
- `document.body.dataset.creator` — server-rendered attribute indicating the platform is in creator mode

## Scenarios

### Regular user who has not completed onboarding is redirected

1. User is authenticated but has not yet seen onboarding (`saw_onboarding` is false).
2. User navigates to any page that is not `/onboarding`, `/signout_confirm`, `/privacy`, or `/admin/creator_settings/new`.
3. The page loads; the client fetches user data.
4. The system detects that onboarding is not skippable.
5. The browser is redirected to `/onboarding?referrer=<current URL>`.

### User who has completed onboarding is not redirected

1. User is authenticated and `saw_onboarding`, `checked_code_of_conduct`, and `checked_terms_and_conditions` are all true.
2. User navigates to any page.
3. The page loads; the client fetches user data.
4. The system detects onboarding is skippable and takes no action.

### User on an excluded page is not redirected

1. User is authenticated but has not completed onboarding.
2. User is currently on `/onboarding`, `/signout_confirm`, `/privacy`, or `/admin/creator_settings/new`.
3. The page loads; the client fetches user data.
4. The system recognises the current path as non-redirectable and takes no action.

### Creator user who has not seen onboarding is redirected to creator settings wizard

1. The platform is running in creator mode (`document.body.dataset.creator === 'true'`).
2. An authenticated user has `saw_onboarding` set to false.
3. User navigates to a page that is not excluded by either the standard or creator-specific exclusion lists.
4. The system redirects the browser to `/admin/creator_settings/new?referrer=<current URL>` instead of `/onboarding`.

### InstantClick transition re-runs the redirect check

1. User navigates between pages using InstantClick (soft navigation).
2. An `InstantClick` `change` event fires.
3. The client fetches fresh user data and reads `shouldRedirectToOnboarding` from localStorage.
4. If the flag is truthy (or absent) and the user has not completed onboarding, the browser is redirected to `/onboarding` (or the creator settings wizard if applicable).
5. If the flag is explicitly `false`, the redirect is suppressed.

## Failures / Exceptions

- If fetching user data or the CSRF token fails, the error is caught and logged to the console via `console.error`; no redirect occurs, and the user remains on the current page.
