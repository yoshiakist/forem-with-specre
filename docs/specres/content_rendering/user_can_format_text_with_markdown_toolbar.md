---
id: "01KJ2XF079Y76ZC5FMC33W6BZB"
name: "user_can_format_text_with_markdown_toolbar"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/javascript/crayons/MarkdownToolbar/MarkdownToolbar.jsx`
- `app/javascript/crayons/MarkdownToolbar/markdownSyntaxFormatters.jsx`
- `app/javascript/crayons/MarkdownToolbar/index.js`
- `app/javascript/utilities/textAreaUtils.js`
- `app/javascript/crayons/MarkdownToolbar/__tests__/MarkdownToolbar.test.jsx` (Test)
- `app/javascript/crayons/MarkdownToolbar/__tests__/markdownSyntaxFormatters.test.js` (Test)

## Functional Overview

The `MarkdownToolbar` component renders a formatting toolbar linked to a target textarea by ID. It exposes a set of formatting actions — bold, italic, link, ordered list, unordered list, heading, quote, code, code block, embed, underline, strikethrough, and line divider — as icon buttons. The number of buttons shown directly in the toolbar varies by screen size (5 on small, 7 on large, 10 on extra-large); remaining formatters are placed in an overflow dropdown menu. Clicking a button or triggering a keyboard shortcut applies or removes the corresponding Markdown syntax around the user's current text selection in the textarea, using `document.execCommand` for undo-stack compatibility with a direct value-update fallback. Image uploads are handled via an integrated `ImageUploader` that inserts a placeholder while uploading and replaces it with the final image Markdown on completion. The toolbar navigation follows the ARIA toolbar/roving-tabindex pattern, with arrow keys cycling through visible buttons and Escape closing the overflow menu.

## Design Intent

`document.execCommand('insertText')` is used despite being deprecated because no standardized replacement API exists yet for inserting text into a textarea while preserving the browser's native undo/redo history. A direct value assignment fallback is provided for environments where `execCommand` throws. The `contentEditable` attribute is temporarily set to `true` on the textarea just long enough to allow `execCommand` to work, then restored to `false`, keeping the element semantically correct outside that narrow window.

## Key Members

- `textAreaId` — ID of the textarea element this toolbar controls; used to obtain a ref via `document.getElementById` inside `useLayoutEffect`.
- `additionalSecondaryToolbarElements` — optional array of extra elements rendered inside the overflow menu alongside the built-in formatter buttons.
- `markdownSyntaxFormatters` — registry object mapping formatter names (e.g. `bold`, `link`, `heading`) to their icon, label, optional keyboard shortcut, and `getFormatting` function that computes the edit to apply.
- `storedCursorPosition` — captures the textarea's `selectionStart`/`selectionEnd` at the moment the image upload button is clicked, so the placeholder can be inserted at the correct position.

## Scenarios

### Applying inline formatting to a text selection

1. The user selects text in the textarea and clicks a toolbar button for an inline format (bold, italic, code, underline, strikethrough, or embed).
2. The toolbar computes the new text by wrapping the selection with the appropriate prefix and suffix characters.
3. The formatted text replaces the selection in the textarea; the cursor remains selecting the originally selected content (now inside the markers).

### Toggling inline formatting off

1. The user selects text that is already wrapped with a known inline prefix and suffix (e.g. `**word**`), then clicks the corresponding toolbar button.
2. The toolbar detects that the selection or its immediate surroundings already carry that formatting.
3. The markers are removed and the bare text is restored; the cursor adjusts accordingly.

### Applying block/multiline formatting

1. The user places the cursor or selects multiple lines, then activates a block formatter (heading, quote, unordered list, ordered list, code block, or line divider).
2. The toolbar adds the appropriate line prefix or block prefix/suffix, inserting any required blank lines before and after the block to satisfy Markdown spacing rules.
3. If the selected text already has that block formatting, the toolbar removes it instead.

### Accessing overflow formatters on smaller screens

1. The user views the editor on a small or medium screen, where the toolbar shows only 5 or 7 core formatters.
2. The user clicks the "More options" overflow button; the remaining formatters appear in a dropdown menu.
3. The user selects a formatter from the dropdown; the overflow menu closes and the formatting is applied to the textarea.

### Inserting an image via upload

1. The user clicks the image upload button; the toolbar records the current cursor position.
2. While the upload is in progress, a `![Uploading image](...)` placeholder is inserted at the cursor position and the textarea dispatches an `input` event to notify any bound state.
3. When the upload succeeds or fails, the placeholder is replaced with the final image Markdown (or an empty string on error); the cursor is adjusted to account for any change in text length.

## Failures / Exceptions

- If `document.execCommand` throws (e.g. in certain browser environments), the toolbar falls back to directly assigning the new value to `textarea.value`. This preserves correctness but loses native undo-queue integration.
- If the `![Uploading image](...)` placeholder has been manually deleted by the user before the upload completes, `handleImageUploadEnd` detects its absence and returns without making any change.
