---
id: "01KJXZTMRF1JY5D0FS8VQV3V8V"
name: "user_can_trigger_autocomplete_in_textarea"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/AutocompleteTriggerTextArea/AutocompleteTriggerTextArea.jsx`
- `app/javascript/crayons/AutocompleteTriggerTextArea/index.js`
- `app/javascript/crayons/AutocompleteTriggerTextArea/__tests__/AutocompleteTriggerTextArea.test.jsx` (Test)

## Functional Overview

`AutocompleteTriggerTextArea` is a Preact component that wraps a standard textarea with configurable trigger-character autocomplete. When the user types a designated trigger character (e.g., `@`), the component enters combobox mode, fetches matching suggestions via a caller-supplied `fetchSuggestions` callback, and displays a floating dropdown positioned near the cursor. The user can navigate suggestions with the keyboard arrow keys, confirm a selection with Enter or a mouse click, and dismiss the dropdown with Escape. On selection, the trigger character and the chosen value are inserted in place of the typed search term. The component can optionally replace a pre-existing textarea element, copying over all its attributes and styles, and supports auto-resize and a configurable maximum suggestion count.

## Design Intent

The component is designed as a generic, reusable primitive that does not embed any domain knowledge about the suggestion content. Callers supply `triggerCharacter` and `fetchSuggestions`, so the same component can back any mention or tag feature. Accessibility is treated as first-class: the textarea is promoted to `role="combobox"` with the full set of ARIA combobox attributes (`aria-haspopup`, `aria-expanded`, `aria-owns`, `aria-activedescendant`) only while combobox mode is active, keeping the DOM clean when autocomplete is idle. The dropdown is rendered into `document.body` via a portal to avoid clipping by overflow-hidden ancestor containers, and its position is computed from the cursor coordinates so it appears directly beneath the search text. On narrow screens the dropdown is anchored to the left edge of the textarea instead of the cursor to prevent it from being clipped.

## Key Members

- `triggerCharacter` — the single character whose entry activates autocomplete mode (e.g., `"@"`)
- `fetchSuggestions(searchTerm)` — async callback supplied by the caller; receives the text typed after the trigger and returns an array of suggestion objects, each with at least a `value` property
- `maxSuggestions` — optional cap on the number of suggestions shown; excess results are silently discarded
- `replaceElement` — optional existing DOM textarea node to be seamlessly replaced by the enhanced component on mount, with all attributes and styles transferred
- `autoResize` — when true, the textarea grows to fit its content using `useTextAreaAutoResize`
- `searchInstructionsMessage` — text shown in the dropdown before the search term reaches the minimum length (2 characters) and announced via an ARIA live region when combobox mode activates
- `isComboboxMode` (state) — true while the user is actively searching after typing the trigger character
- `suppressPopover` (state) — temporarily hides the dropdown after Escape without exiting combobox mode; cleared on any subsequent keypress that is not Escape
- `ignoreBlur` (state) — prevents the blur handler from exiting combobox mode when a dropdown option is clicked with the mouse, since clicking an option causes the textarea to lose focus momentarily
- `activeDescendentIndex` (state) — zero-based index of the keyboard-focused suggestion, or null when no suggestion is highlighted

## Scenarios

### Trigger character activates combobox mode

1. The textarea is initially in plain textbox mode with no ARIA combobox attributes.
2. The user types the configured trigger character.
3. The component detects the trigger via `getAutocompleteWordData` and sets `isComboboxMode` to true.
4. The textarea gains `role="combobox"`, `aria-haspopup="listbox"`, `aria-expanded="true"`, and `aria-owns` pointing to the listbox.
5. An ARIA live region announces the `searchInstructionsMessage` to assistive technologies.

### Dropdown populates once search term reaches minimum length

1. The user types the trigger character followed by at least two additional characters.
2. The component extracts the search term (text between the trigger character and the cursor) and calls `fetchSuggestions` with it.
3. Suggestions returned by `fetchSuggestions` are stored; if `maxSuggestions` is set, only the first `maxSuggestions` entries are kept.
4. A floating dropdown is rendered into the page body, positioned below the cursor (or below the textarea's left edge on small screens).
5. Each suggestion appears as a listbox option with `role="option"`.

### User navigates and selects a suggestion with the keyboard

1. While the dropdown is visible, the user presses ArrowDown to move focus to the first option; `aria-activedescendant` on the textarea updates accordingly and the option receives `aria-selected="true"`.
2. Pressing ArrowDown again advances to the next option; pressing ArrowUp moves back.
3. When the user presses Enter with an option highlighted, the search term (from the trigger character to the cursor) is replaced in the textarea with `<triggerCharacter><suggestion.value> ` (including a trailing space).
4. The component exits combobox mode: the dropdown closes and all combobox ARIA attributes are removed.

### User selects a suggestion by clicking

1. The user clicks a suggestion option in the dropdown.
2. A `mousedown` event on the option sets `ignoreBlur` to true so the textarea blur does not prematurely close the dropdown.
3. The click handler calls `selectSuggestion`, which focuses the textarea, sets the selection range to cover the current search term, and inserts the replacement text via `document.execCommand('insertText')` (falling back to direct value manipulation if `execCommand` is unavailable).
4. The component exits combobox mode and the dropdown closes.

### User dismisses the dropdown with Escape

1. While the dropdown is visible, the user presses Escape.
2. The component sets `suppressPopover` to true; the dropdown disappears but `isComboboxMode` remains true.
3. The next keystroke (other than Escape) clears `suppressPopover` and the dropdown can reappear if the trigger condition is still met.

### Component replaces an existing textarea on mount

1. A caller renders the component with `replaceElement` pointing to an existing DOM textarea.
2. On mount, the component copies all HTML attributes and computed CSS styles from the original element onto the new enhanced textarea, then removes the original from the DOM.
3. The enhanced textarea is immediately focused and the page presents exactly one textarea element with the original element's identity and appearance.
