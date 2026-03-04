---
id: "01KJV7320ZN2XMTYR9W58S7BBX"
name: "editor_shows_accessibility_suggestions_in_preview"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/javascript/article-form/components/AccessibilitySuggestions.jsx`
- `app/javascript/article-form/components/__tests__/AccessibilitySuggestions.test.jsx` (Test)
- `app/javascript/article-form/components/Preview.jsx`
- `app/javascript/article-form/articleForm.jsx`

## Functional Overview

When a user opens the preview panel in the article editor, the editor runs the article's Markdown body through a set of custom markdownlint rules. If any accessibility violations are found — such as images with missing or default alt text, or heading-level issues — the preview panel displays an `AccessibilitySuggestions` notice above the article title. The notice lists up to three suggestions, favouring image-related errors (which are considered more impactful) before filling remaining slots with other error types. Each suggestion includes a contextual description and a "Learn more" link pointing to the relevant documentation.

## Design Intent

Image accessibility errors (`no-default-alt-text`, `no-empty-alt-text`) are given priority over heading-level errors because missing or meaningless alt text is a higher-impact accessibility barrier. The hard cap of three suggestions avoids overwhelming the author while still surfacing the most important issues. The notice is suppressed entirely when there are form submission errors, so that error messages are not competing with accessibility hints.

## Key Members

- `MAX_SUGGESTIONS: 3` — maximum number of suggestions rendered in the UI
- `markdownLintErrors: LintError[]` — array of markdownlint error objects held in `ArticleForm` state, each carrying `ruleNames`, `errorContext`, and `errorDetail`
- `extractRelevantErrors(lintErrors)` — splits errors into image and other buckets, truncates each to fit within `MAX_SUGGESTIONS`, and returns image errors first

## Scenarios

### Accessibility suggestions appear when preview loads with violations

1. The user clicks the preview button while the article body contains accessibility violations (e.g., an image with no alt text).
2. `ArticleForm` fetches the rendered preview from the server and, on success, calls `fetchMarkdownLint` to load the markdownlint library if needed, then runs `lintMarkdown` against the current body Markdown.
3. The resulting lint errors are stored in `markdownLintErrors` state.
4. The `Preview` component renders `AccessibilitySuggestions` with those errors, and the notice appears above the article title with a list of up to three suggestions.

### Image errors are prioritised when three or more image violations exist

1. The article body contains three or more image-related violations (e.g., multiple images with missing or empty alt text) alongside heading violations.
2. When the preview loads and lint runs, `extractRelevantErrors` collects all image errors first and truncates the list to three.
3. The suggestions panel shows only the three image-related errors; heading errors are omitted entirely.

### Remaining suggestion slots are filled by other errors when fewer than three image errors exist

1. The article body contains fewer than three image-related violations and one or more heading-level violations.
2. `extractRelevantErrors` places the image errors first, then fills the remaining slots (up to the three-item cap) with heading errors.
3. The suggestions panel shows the image errors followed by as many heading errors as fit within the cap.

### No suggestions panel when there are no lint errors

1. The article body contains no accessibility violations.
2. `markdownLintErrors` remains empty after linting.
3. `Preview` skips rendering `AccessibilitySuggestions`; the preview header shows only the article title and tags.

### Suggestions panel is suppressed when submission errors are present

1. The preview is shown alongside a form submission error (e.g., a validation failure returned by the server).
2. `Preview` checks for errors before checking `markdownLintErrors`; because errors are present, `AccessibilitySuggestions` is not rendered.
3. Only the submission error list is displayed in the preview header.
