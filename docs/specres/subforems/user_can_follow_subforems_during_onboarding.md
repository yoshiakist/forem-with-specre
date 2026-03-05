---
id: "01KHYYD4RVEHXFA0M3F62W5PQD"
name: "user_can_follow_subforems_during_onboarding"
status: "draft"
---

## Related Files

- app/javascript/onboarding/components/FollowSubforems.jsx
- app/javascript/packs/signupSubforemStorage.js
- app/javascript/packs/signupSubforemStorage.jsx

## Functional Overview

During the onboarding flow (v2), new users can select which subforems to follow. If the user signed up from a specific subforem, that subforem's ID is persisted in localStorage via a signup storage script. The `FollowSubforems` Preact component fetches all subforems from the API, displays them in a selectable grid (excluding root subforems), highlights the original signup subforem, and allows multi-selection. On completion, the component follows all selected subforems via the `/follows` endpoint and advances the onboarding progress.

## Scenarios

### User selects subforems during onboarding

1. User reaches the "Follow Subforems" step in the onboarding flow
2. System fetches subforems from `/api/subforems` and displays non-root subforems in a grid
3. If the user signed up from a specific subforem, that subforem is visually highlighted
4. User selects one or more subforems by clicking on their cards
5. The subtitle updates to show the number of selected subforems

### User completes subforem selection

1. User clicks the "Continue" button after selecting subforems
2. System sends a POST to `/follows` for each selected subforem
3. System clears the `signup_subforem_id` from localStorage
4. System updates the user's last onboarding page via PATCH to `/onboarding`
5. User proceeds to the next onboarding step

### Signup subforem is remembered across pages

1. When a user lands on a signup page with a `signup_subforem` query parameter, the script stores the subforem ID in localStorage under the key `signup_subforem_id`
2. The `FollowSubforems` component retrieves this ID on mount to pre-highlight the originating subforem
