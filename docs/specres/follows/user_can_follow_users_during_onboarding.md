---
id: "01KJ1XDS1H71C80XA3MK3J78ZX"
name: "user_can_follow_users_during_onboarding"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/javascript/onboarding/components/FollowUsers.jsx`
- `app/javascript/onboarding/components/__tests__/FollowUsers.test.jsx` (Test)

## Functional Overview

During onboarding, the `FollowUsers` step presents the new user with a curated list of suggested users and organizations to follow. On mount, it fetches suggested followees from `GET /onboarding/users_and_organizations` and pre-selects all of them. The user can individually toggle each followee or use a "Select all / Deselect all" toggle. A live follow-count summary updates as selections change. When the user proceeds, selected followees are submitted to `POST /api/follows` grouped by type (users and organizations separately), and the onboarding flow advances to the next slide. If no followees are selected the navigation button changes from "Continue" to "Skip for now".

## Key Members

- `follows` — full list of suggested followees fetched from the server; each item carries `id`, `name`, `profile_image_url`, `summary`, and `type_identifier` (`"user"` or `"organization"`).
- `selectedFollows` — subset of `follows` currently chosen by the user; starts equal to the full list (all pre-selected).
- `loading` — boolean that hides the spinner once the fetch completes.

## Scenarios

### Initial load: suggested followees are fetched and pre-selected

1. The component mounts and fires a GET request to `/onboarding/users_and_organizations`.
2. While the response is pending a spinner is displayed.
3. On success, the full list of returned followees is stored and every item is pre-selected.
4. The spinner is hidden and each followee is rendered with a "Following" checkbox label.
5. Simultaneously, a PATCH to `/onboarding` records that the user has reached the follow-users page.

### User toggles an individual followee

1. The user clicks the checkbox label for a followee that is currently selected.
2. That followee is removed from the selected set; its label changes to "Follow".
3. The follow-count summary updates to reflect the new count and, if nothing is selected, the navigation button reads "Skip for now".
4. Clicking the same followee again re-adds it to the selected set and the label returns to "Following".

### User uses the Select all / Deselect all toggle

1. When all followees are selected the toggle button reads "Deselect all"; clicking it clears the entire selection.
2. When fewer than all followees are selected the toggle reads "Select all N" (or "Select 1" for a single item); clicking it selects all.
3. After toggling, the follow-count summary and navigation button text update accordingly.

### User proceeds with selected followees

1. The user clicks the "Continue" button with at least one followee selected.
2. The selected followee IDs are grouped by `type_identifier` into `users` and `organizations` arrays.
3. A POST request is sent to `/api/follows` with the grouped IDs and a CSRF token.
4. The `next` callback supplied by the parent is invoked, advancing the onboarding flow.

### User skips without selecting anyone

1. With no followees selected the navigation button reads "Skip for now".
2. Clicking it triggers `handleComplete`, which posts an empty body to `/api/follows` and calls `next()` to proceed.

## Failures / Exceptions

- If the `/onboarding/users_and_organizations` fetch fails or returns an unexpected response, no error handling is present; the component will remain in the loading state indefinitely.
