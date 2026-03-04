---
id: "01KJV0FGGM94SH8KZS9W17794A"
name: "editor_warns_before_closing"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/javascript/article-form/components/Close.jsx`
- `app/javascript/article-form/articleForm.jsx`
- `app/javascript/article-form/components/__tests__/Close.test.jsx` (Test)

## Functional Overview

The editor header contains a `Close` button (rendered by `Close.jsx`). When clicked, it calls `displayModal()` on `ArticleForm`, which opens a confirmation modal (`isModalOpen: true`). The modal lets the user confirm navigation away or cancel. Additionally, `ArticleForm` registers a `beforeunload` listener on mount that calls `localStoreContent`, which persists the current form state to `localStorage` before the browser unloads. If the user navigates without clicking Close (e.g., via browser back), there is no browser-native `beforeunload` prompt; the content is merely saved to localStorage silently.

## Design Intent

The in-editor close modal provides a deliberate pause before discarding unsaved work, reducing accidental data loss. The `beforeunload` handler pairs with the editor's localStorage restore so that content survives any navigation, even without a modal confirmation.

## Key Members

- `Close({ displayModal })` — renders an icon button that calls `displayModal()` on click
- `ArticleForm#displayModal` / `isModalOpen` state — controls the confirmation modal visibility
- `ArticleForm#localStoreContent` — persists `title`, `tagList`, `bodyMarkdown`, `mainImage`, `videoSourceUrl`, `updatedAt` to `localStorage`
- `componentDidMount` / `componentWillUnmount` — attach/detach the `beforeunload` listener

## Scenarios

### Author clicks Close with unsaved changes

1. Author has unsaved edits and clicks the Close (×) button in the editor header.
2. `Close` calls `displayModal()`; `ArticleForm` sets `isModalOpen: true`.
3. A confirmation modal appears asking whether to leave the editor.
4. If the author confirms, the browser navigates away (typically to `/`).
5. If the author cancels, the modal closes and editing continues.

### Author navigates away without clicking Close

1. Author navigates away via browser back or a link.
2. The `beforeunload` listener fires `localStoreContent`.
3. Current form state is saved to `localStorage`; no browser dialog is shown.
4. On the next visit to the same editor URL, the form restores the saved draft.

## Failures / Exceptions

- If `localStorage` is full or unavailable, `localStoreContent` silently fails and no draft is saved.
