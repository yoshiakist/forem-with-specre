---
id: "01KJV72PBDYQK52A1J9HY0CEHX"
name: "editor_shows_contextual_help_and_formatting_guidance"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/javascript/article-form/articleForm.jsx`
- `app/javascript/article-form/components/Help/index.jsx`
- `app/javascript/article-form/components/Help/ArticleFormTitle.jsx`
- `app/javascript/article-form/components/Help/ArticleTips.jsx`
- `app/javascript/article-form/components/Help/BasicEditor.jsx`
- `app/javascript/article-form/components/Help/EditorFormattingHelp.jsx`
- `app/javascript/article-form/components/__tests__/Help.test.jsx` (Test)

## Functional Overview

The article editor renders a contextual help sidebar that changes its content based on which form field the author currently has focused. The `Help` container component receives a `helpFor` string (set by `switchHelpContext` in `ArticleForm` when a field receives focus) and a `version` flag, and uses these to decide which help panel to display. When the author focuses the title field, tips for writing an effective title appear. When the body editor is focused, Markdown formatting guidance with an inline syntax cheat-sheet and links to Liquid tag and front-matter reference modals is shown. When the tag input is focused, tag-entry help appears. When the editor-actions area is focused, general publishing tips are shown. In the legacy basic editor (v1), all three panels — basic-editor notice, formatting help, and publishing tips — are displayed simultaneously regardless of focus. The help sidebar is hidden entirely while the preview panel is active.

## Design Intent

The `helpFor` identifier is set to the DOM element's `id` value at the point of focus, so the Help component can map field identity to panel type without additional coupling. This keeps the routing logic simple: a single string prop drives all switching. The `helpPosition` value (the focused element's Y coordinate) is passed so the sticky sidebar can be anchored near the field the author is working on. Modals for Liquid tags, Markdown syntax, and Jekyll front matter are rendered lazily — only when the author explicitly requests them — by reading pre-rendered HTML from hidden DOM elements injected server-side.

## Key Members

- `helpFor: string` — identifier of the currently focused form field; drives which help panel renders (`"article-form-title"`, `"tag-input"`, `"article_body_markdown"`, `"editor-actions"`)
- `helpPosition: number` — Y-coordinate of the focused field, used to position the sticky help sidebar
- `version: string` — editor version (`"v1"` or `"v2"`); v1 always shows all panels, v2 shows only the panel matching `helpFor`
- `previewShowing: boolean` — when true, the entire help sidebar is suppressed
- `helpSectionVisibility: object` — local state tracking which of the three detail modals (`liquidShowing`, `markdownShowing`, `frontmatterShowing`) is open

## Scenarios

### Help sidebar is hidden during preview

1. The author activates the article preview.
2. `previewShowing` is set to true and passed to the `Help` component.
3. The help sidebar wrapper is not rendered; no help panel is visible.

### Title field focused shows title-writing tips

1. The author focuses the article title input (id `"article-form-title"`).
2. `ArticleForm.switchHelpContext` fires and sets `helpFor` to `"article-form-title"`.
3. The `Help` component renders `ArticleFormTitle`, which lists guidance on writing a compelling, search-friendly post title.
4. All other help panels remain hidden.

### Body editor focused shows Markdown formatting guidance

1. The author focuses the Markdown body textarea (id `"article_body_markdown"`).
2. `helpFor` is set to `"article_body_markdown"`.
3. The `Help` component renders `EditorFormattingHelp`, which lists Markdown syntax, an expandable cheat-sheet table, embed instructions, and links to open the Liquid tags and Markdown detail modals.
4. All other help panels remain hidden.

### Tag input focused shows tag-entry help

1. The author focuses the tag input (id `"tag-input"`).
2. `helpFor` is set to `"tag-input"`.
3. The `Help` component renders the `TagInput` help panel.
4. All other help panels remain hidden.

### Basic editor (v1) shows all panels regardless of focus

1. The article is opened with the legacy v1 editor.
2. `version` is `"v1"` and is passed to `Help`.
3. Regardless of `helpFor`, the sidebar renders three panels simultaneously: `BasicEditor` (informing the author they are using the basic Markdown editor and linking to UX settings to switch), `EditorFormattingHelp`, and `ArticleTips` (publishing tips).

### Author opens a formatting detail modal

1. While the formatting help panel is visible, the author clicks a link such as "Markdown" or "See a list of supported embeds".
2. `openModal` is called with the corresponding key (`"markdownShowing"` or `"liquidShowing"`).
3. `helpSectionVisibility` is updated to show only that modal.
4. A `Modal` overlay appears, rendering HTML sourced from a pre-existing hidden DOM element (e.g., `editor-markdown-help`).
5. The author closes the modal; `closeModal` resets the visibility flag and the overlay is removed.

## Failures / Exceptions

- If the hidden DOM element referenced by a modal selector (e.g., `editor-liquid-help`) does not exist, `innerHTML` resolves to `undefined` and the modal body renders empty rather than throwing an error.
