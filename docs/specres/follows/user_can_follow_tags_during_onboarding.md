---
id: "01KJ1XAVJ8QCYY0G6ETZ9GF5K2"
name: "user_can_follow_tags_during_onboarding"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/javascript/onboarding/components/FollowTags.jsx`
- `app/javascript/onboarding/components/__tests__/FollowTags.test.jsx` (Test)
- `spec/requests/onboardings_spec.rb` (Test)

## Functional Overview

During onboarding, the `FollowTags` component presents a curated list of tags fetched from `GET /onboarding/tags` and allows the user to select any number of tags they are interested in. When the slide loads, the component also records the user's progress by sending a `PATCH /onboarding` request with the page name. If a previously-read article is stored in `localStorage`, that article's tags are pre-selected. The user can toggle individual tags by clicking or via keyboard (Enter/Space). Upon completing the step, each selected tag is submitted to `POST /follows` as a follow relationship, and — if the user opted in — a `PATCH /onboarding/notifications` request is sent to enable the periodic email digest. The component also allows the user to skip without selecting any tags.

## Design Intent

The email-digest checkbox uses a custom container element (`.onboarding-email-digest`) as the primary click/keyboard target rather than the checkbox itself. This ensures a larger accessible hit area while preventing double-toggle when the checkbox input itself is clicked directly (via `stopPropagation` on the checkbox's click handler). The initial state of the digest opt-in is derived from a `data-default_email_optin_allowed` attribute on `document.body`, allowing the server to pre-configure the default per-community.

## Key Members

- `allTags` — full list of tag objects loaded from `GET /onboarding/tags`
- `selectedTags` — array of tag objects the user has toggled on
- `email_digest_periodic` — boolean tracking whether the user opted into the periodic email digest; initialized from `document.body.dataset.default_email_optin_allowed`
- `article` — optional article object hydrated from `localStorage` (`onboarding_article`) used to pre-select relevant tags

## Scenarios

### Tags are loaded and displayed on mount

1. The component mounts and immediately fetches the tag list from `GET /onboarding/tags`.
2. The response is stored as `allTags` and each tag is rendered as a clickable item showing the tag name and its post count.
3. Simultaneously, a `PATCH /onboarding` request is sent recording that the user reached the "v2: follow tags page".
4. If `localStorage` contains an `onboarding_article` entry, the tags matching that article are pre-selected.

### User selects and deselects tags

1. The user clicks a tag item (or presses Enter or Space while it is focused).
2. If the tag is not already selected, it is added to `selectedTags` and the item renders with a selected visual style.
3. The follow count label updates to reflect the current number of selected tags (e.g., "1 tag selected", "2 tags selected").
4. If the tag is already selected, clicking it again removes it from `selectedTags` and the item reverts to the unselected style.
5. When at least one tag is selected, the navigation button changes from "Skip for now" to "Continue".

### User completes the step with selected tags

1. The user clicks the "Continue" navigation button after selecting one or more tags.
2. For each tag in `selectedTags`, a `POST /follows` request is sent with `followable_type: "Tag"`, `followable_id`, and `verb: "follow"`.
3. All follow requests are issued concurrently via `Promise.all`.
4. After all follows succeed, if `email_digest_periodic` is true a `PATCH /onboarding/notifications` request is sent with `email_digest_periodic: true`.
5. Once the notifications request (or its no-op alternative) resolves successfully, the `next` prop callback is invoked to advance the onboarding flow.

### User skips without selecting tags

1. No tags are selected (the "Skip for now" button is visible).
2. The user clicks "Skip for now", which invokes `handleComplete`.
3. Because `selectedTags` is empty, `Promise.all` resolves immediately with no network requests for follows.
4. If `email_digest_periodic` is true, the notifications patch is still sent; otherwise the flow advances directly.
5. The `next` callback is called, moving to the next onboarding step.

### User toggles the periodic email digest opt-in

1. The `.onboarding-email-digest` container is visible below the tag list.
2. Clicking the container (or pressing Enter or Space while it is focused) toggles the `email_digest_periodic` checkbox state.
3. Clicking the checkbox input directly stops propagation so the container handler does not fire a second time.
4. The checkbox reflects the updated state, and `email_digest_periodic` in component state is updated accordingly.

## Failures / Exceptions

- If the `PATCH /onboarding/notifications` response is not `ok`, the `next` callback is not invoked and the user remains on the step (the promise chain checks `response.ok` before advancing).
