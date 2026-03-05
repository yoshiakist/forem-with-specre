---
id: "01KJXZPHA4ZGKYT9TKD0PD211R"
name: "user_can_enter_multiple_values_in_input"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/MultiInput/MultiInput.jsx`
- `app/javascript/crayons/MultiInput/__tests__/MultiInput.test.jsx` (Test)

## Functional Overview

The `MultiInput` component lets a user build a list of text values inside a single input field. The user types a value and confirms it by pressing Enter, comma, or space; the confirmed value is then displayed as a removable pill alongside the input. Pressing Backspace in an empty input pulls the most-recently-added pill back into the text field for editing. Each pill is rendered via a replaceable `SelectionTemplate`, which exposes both an edit callback and a deselect (remove) callback. An optional `validationRegex` controls whether a confirmed value is marked valid or invalid, and an optional `inputRegex` restricts which characters can be typed at all. A visually-hidden live region announces additions and removals to screen-reader users.

## Design Intent

Separating the "confirm" gesture (Enter / comma / space) from the "submit" gesture makes it natural to compose a list before submitting a form. Using a replaceable `SelectionTemplate` allows consuming teams to customise the visual appearance of pills without forking the core input logic. Inline editing (Backspace-to-edit rather than delete-and-retype) reduces friction when a user wants to correct a minor typo.

## Key Members

- `items: Array<{ value: string, valid: boolean }>` — the ordered list of confirmed values currently displayed as pills
- `editValue: string | null` — the text pre-loaded into the input when a pill is being edited; `null` when not in edit mode
- `inputPosition: number | null` — the list index at which the inline input is currently positioned; `null` means the input is appended after all pills
- `inputRegex: RegExp` — filters individual keystrokes; keystrokes that do not match are suppressed
- `validationRegex: RegExp` — tested against the whole value on confirmation; non-matching values receive the `c-input--multi__selected-invalid` class and the accessible description "Invalid entry"
- `SelectionTemplate: Component` — Preact component used to render each pill; receives `name`, `onEdit`, `onDeselect`, `valid`, and `enableValidation` props

## Scenarios

### User confirms a value with Enter, comma, or space

1. User focuses the input and types a non-empty value.
2. User presses Enter, comma, or space.
3. The component adds the value to the pill list and clears the input field.
4. The new pill appears with an edit button and a remove button.
5. A screen-reader live region announces the addition.

### User removes a pill by clicking its remove button

1. A confirmed value is displayed as a pill with a remove button.
2. User clicks the remove button on the pill.
3. The pill disappears from the list.
4. The screen-reader live region announces the removal.
5. The text input receives focus.

### User edits a pill by clicking its edit button

1. A confirmed value is displayed as a pill with an edit button.
2. User clicks the edit button on the pill.
3. The pill is removed from the list and its text is placed back into the input field.
4. The input is focused and the cursor is positioned at the end of the text.
5. User modifies the text and confirms again (Enter / comma / space / blur), re-adding it as a pill in the same list position.

### User presses Backspace in an empty input to edit the previous pill

1. The input is empty (no partially-typed text).
2. User presses Backspace.
3. The last pill (or the pill immediately before the current input position) is removed from the list and its text is loaded into the input.
4. The input is focused with the cursor at the end of the restored text.

### Invalid value is marked but still accepted

1. A `validationRegex` is provided to the component.
2. User types a value that does not satisfy the regex and confirms it.
3. The value is added to the pill list with `valid: false`.
4. The pill renders with the invalid style class and the accessible description "Invalid entry".
5. A value that does satisfy the regex is added with `valid: true` and receives no invalid description.

## Failures / Exceptions

- Whitespace-only input is ignored; confirming via any delimiter when the trimmed value is empty produces no pill.
- When `inputRegex` is provided, individual keystrokes that do not match the pattern are suppressed entirely, preventing invalid characters from appearing in the field.
- Pressing Backspace in an empty input when there are no pills (or when the input is already at position 0) has no effect.
