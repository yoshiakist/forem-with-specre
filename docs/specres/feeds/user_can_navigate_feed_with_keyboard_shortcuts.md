---
id: "01KJ24EJFAY39BP4S14QX5H5FH"
name: "user_can_navigate_feed_with_keyboard_shortcuts"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/javascript/packs/homePageFeedShortcuts.jsx`
- `app/javascript/shared/components/useListNavigation.js`
- `app/javascript/shared/components/useKeyboardShortcuts.js`
- `app/javascript/shared/components/__tests__/useListNavigation.test.js` (Test)
- `app/javascript/shared/components/__tests__/useKeyboardShortcuts.test.jsx` (Test)

## Functional Overview

On the home page feed, users can navigate between story cards using the keyboard. Pressing `j` moves focus to the next story, and `k` moves focus to the previous one. If no story is currently focused, the first visible story in the viewport is selected. When focus moves outside the visible area, the page scrolls to bring the story into view. Additionally, pressing `b` while a story is focused bookmarks (saves) that story by triggering its save button. These shortcuts are inactive when the user is typing in a form field, and they are wired up at page load by rendering `ListNavigation` and `KeyboardShortcuts` components into the main content root.

## Design Intent

The keyboard shortcut system is split into two layers of abstraction. `useKeyboardShortcuts` is a generic hook that maps key combinations — including modifier keys and sequential key chains — to callbacks, while `useListNavigation` builds on top of it to provide the specific j/k navigation pattern. This separation allows keyboard shortcut handling to be reused elsewhere in the application without coupling it to feed-specific behavior. The waterfall item container support in `useListNavigation` handles feeds that load articles in batches inside nested wrapper elements, enabling seamless navigation across pagination boundaries.

## Key Members

- `itemSelector` — CSS selector identifying the top-level container of each navigable story item (e.g., `.crayons-story`)
- `focusableSelector` — CSS selector for the element within each item that receives focus (e.g., `a.crayons-story__hidden-navigation-link`)
- `waterfallItemContainerSelector` — optional CSS selector for paginated or nested batch containers (e.g., `div.paged-stories,div.substories`)
- `shortcuts` — map of key identifiers or key sequences to handler callbacks; key strings use the pattern `KeyCode`, `modifier+KeyCode`, or `KeyA~KeyB` for chained presses
- `timeout` — milliseconds allowed between keys in a chain before the chain resets; defaults to `0` (no delay)

## Scenarios

### User navigates down the feed with the j key

1. The home page renders with `ListNavigation` and `KeyboardShortcuts` mounted into the main content root.
2. No story is currently focused.
3. The user presses `j` (`KeyJ`).
4. The system selects the first story visible in the viewport and moves keyboard focus to its hidden navigation link.
5. The user presses `j` again; focus moves to the next story in the list.
6. If the newly focused story is outside the viewport, the page scrolls so the story is visible with a 64px top offset.

### User navigates up the feed with the k key

1. Focus is on a story that is not the first item in the list.
2. The user presses `k` (`KeyK`).
3. Focus moves to the previous story's navigation link.
4. If already at the top of the list, focus stays on the first story.

### User bookmarks a story with the b key

1. Focus is on a story card (i.e., the active element is inside a `.crayons-story` element).
2. The user presses `b`.
3. The handler finds the closest `.crayons-story` ancestor of the focused element and clicks its `button[id^=article-save-button-]`.
4. The story is saved or unsaved according to the current save state.

### Shortcut is suppressed inside a form field

1. The user has focus inside a text input, textarea, select, or content-editable element.
2. The user presses `j`, `k`, or `b` without any modifier key held.
3. No navigation or bookmark action is taken; the key event is handled by the form field normally.

### Navigation across waterfall (paginated) containers

1. The feed renders stories in a flat list followed by one or more paginated batch containers (`div.paged-stories` or `div.substories`).
2. The user presses `j` repeatedly until focus reaches the last story before a waterfall container.
3. Pressing `j` again moves focus into the first story inside the waterfall container.
4. Pressing `k` from the first story inside the waterfall container moves focus back to the story immediately preceding the container.
