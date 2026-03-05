---
id: "01KJXZPXJRX88PHAXM110J8W95"
name: "user_can_search_and_select_multiple_options"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/MultiSelectAutocomplete/MultiSelectAutocomplete.jsx`
- `app/javascript/crayons/MultiSelectAutocomplete/index.js`
- `app/javascript/crayons/MultiSelectAutocomplete/__tests__/MultiSelectAutocomplete.test.jsx` (Test)

## Functional Overview

`MultiSelectAutocomplete` is a generic Preact component that lets a user search for and select multiple items from a dynamically fetched or statically provided list. As the user types into the combobox input, suggestions are fetched via a debounced callback and displayed in a dropdown listbox. The user can select items by clicking, pressing Enter after keyboard-navigating the list, or pressing Space or Comma to accept the current input text. Each selected item appears as a chip in the input area and can be edited back into the text field or removed entirely. The component enforces an optional maximum selection count, restricts input to alphanumeric characters, and announces every addition and removal to screen readers through an `aria-live` region.

## Design Intent

The combobox pattern is built to ARIA combobox / listbox conventions so that keyboard-only and screen reader users receive a fully accessible multi-select experience without custom widget frameworks. Suggestions are debounced to avoid redundant network requests while the user is still typing. Selections are maintained in component state rather than a native `<select>` so the chip-based UI and inline edit mode can be supported. The hidden `aria-live="assertive"` list mirrors the selection state and provides instant confirmation messages ("Selected items: …") to assistive technology without disrupting visual focus.

## Key Members

- `fetchSuggestions: (searchTerm: string) => Promise<Array<{name: string}>>` — caller-supplied async function that returns matching option objects for the current search term
- `staticSuggestions: Array<{name: string}>` — pre-defined options shown when the input is empty and focused, before any search term is entered
- `maxSelections: number` — optional cap on how many items can be selected simultaneously
- `allowUserDefinedSelections: boolean` — when true, the user may add free-text entries that do not match any fetched suggestion
- `SuggestionTemplate` / `SelectionTemplate` — optional Preact components for rendering suggestion list items and selected chips; defaults fall back to `DefaultSelectionTemplate`
- `onSelectionsChanged: (selections: Array) => void` — callback invoked every time the selection list changes, enabling parent components to react to state changes
- `activeDescendentIndex` (internal state) — tracks which suggestion is highlighted during keyboard navigation and drives `aria-activedescendant`
- `ignoreBlur` (internal state) — suppresses the blur handler when the user clicks a dropdown option so the mousedown-driven selection is not canceled

## Scenarios

### User types to search and selects an option from the dropdown

1. User focuses the input; if `staticSuggestions` are provided and the input is empty, they appear immediately in the listbox.
2. User begins typing alphanumeric characters; the input value is forwarded to `fetchSuggestions` after a debounce delay.
3. Matching suggestions returned by `fetchSuggestions` replace the listbox contents (already-selected items are excluded from the list).
4. User clicks a suggestion or presses ArrowDown/ArrowUp to highlight one and then presses Enter.
5. The selected item is added as a chip inside the combobox wrapper, the text input is cleared, and `onSelectionsChanged` is called with the updated array.
6. The screen reader live region announces the newly added item.

### User selects by pressing Space or Comma

1. User has typed a search term that matches a suggestion name exactly.
2. User presses Space or Comma; the text before the delimiter is matched against the current suggestions.
3. If a match is found, the item is selected immediately without requiring dropdown navigation.
4. If `allowUserDefinedSelections` is true and no suggestion matches, the typed text itself becomes a new selection.

### User edits a previously selected chip

1. User clicks the "Edit" button on a chip, or presses Backspace while the input is empty.
2. The chip is removed from the selection list and its text is placed back into the input field with the cursor at the end.
3. The input resizes dynamically to fit the restored text and is focused.
4. The user can modify the text and re-select by pressing Enter, Space, Comma, or clicking a suggestion.

### User removes a selected chip

1. User clicks the "Remove" button on a chip.
2. The item is removed from the selection list, `onSelectionsChanged` is called, and the screen reader live region announces the removal.
3. Focus returns to the text input.

### Maximum selection limit is reached

1. The component is configured with `maxSelections`; once that count is reached after a selection, the input's `aria-disabled` attribute is set to `"true"` and its placeholder is cleared.
2. A visible message such as "Only N selections allowed" appears beneath the combobox.
3. Further typing does not trigger suggestion fetches or open the dropdown.
4. Pressing Space or Comma with text in the input does not add a new selection.
5. If the user removes a chip, the limit-reached state clears and normal input behavior resumes.

### Input is blurred without selecting

1. If the current input value matches a suggestion exactly, the item is auto-selected on blur.
2. If `allowUserDefinedSelections` is true and no suggestion matches, the typed text is auto-selected on blur.
3. Otherwise the input is cleared on blur without creating a selection.

## Failures / Exceptions

- Special characters (anything not matching `[a-zA-Z0-9]`) are rejected by `handleKeyDown`; the keydown event is prevented so they never appear in the input.
- If the user types a value that is already selected and presses Space or Comma, the input is cleared without duplicating the selection.
- If `fetchSuggestions` resolves after the input has already been cleared (e.g., the user selected an item while the request was in flight), the stale results are discarded.
- When `allowUserDefinedSelections` is true and `fetchSuggestions` returns an empty array, the current search term is surfaced as the sole suggestion so the user can still select it.
