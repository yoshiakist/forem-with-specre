---
id: "01KJTZVFN07Y5FR14D7Y40J9F5"
name: "author_previews_article_in_editor"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/articles_controller.rb`
- `app/javascript/article-form/articleForm.jsx`
- `app/javascript/article-form/actions.js`
- `app/javascript/article-form/components/Preview.jsx`
- `app/javascript/article-form/components/LoadingPreview.jsx`
- `app/javascript/article-form/components/Header.jsx`
- `app/javascript/article-form/components/__tests__/Preview.test.jsx` (Test)
- `app/javascript/article-form/components/__tests__/LoadingPreview.test.jsx` (Test)
- `spec/requests/articles/articles_spec.rb` (Test)

## Functional Overview

When authoring an article, the author can toggle a live preview of the post without leaving the editor. Clicking the preview tab (or pressing the keyboard shortcut) triggers a POST to `/articles/preview` with the current markdown body. The server renders the markdown through `ContentRenderer`, extracts front-matter fields (title, tags, cover image), and returns processed HTML along with those metadata fields as JSON. While the network request is in flight the editor swaps the editing form for a `LoadingPreview` skeleton that mirrors the article layout, optionally showing a cover-image placeholder if the article has a main image attached. Once the response arrives, the full `Preview` component renders the article header (cover image or video embed, title, and tag links), the rendered HTML body, any validation errors, and any markdown accessibility lint warnings. Toggling preview off restores the editing form. Unauthenticated requests to the preview endpoint receive a 401 Unauthorized response.

## Key Members

- `previewShowing: boolean` — tracks whether the editor is in preview mode
- `previewLoading: boolean` — true while the preview request is in flight
- `previewResponse: { processed_html, title, tags, cover_image }` — server response stored in `ArticleForm` state
- `fetchPreview()` — toggles preview off when already showing; otherwise calls `previewArticle()` and shows loading state
- `previewArticle(payload, successCb, failureCb)` — POSTs `article_body` to `POST /articles/preview` and invokes the appropriate callback
- `LoadingPreview` `version` prop — `'cover'` shows a cover-image scaffold; `'default'` omits it

## Scenarios

### Author opens preview for the first time

1. The author is on the article editor with some markdown content written.
2. The author clicks the "Preview" tab in the editor header or uses the keyboard shortcut (OS modifier + Shift + P).
3. The editor immediately shows the `LoadingPreview` skeleton. If the article has a cover image attached, the skeleton includes a cover-image placeholder area.
4. A POST request is sent to `/articles/preview` with the current markdown body.
5. The server renders the markdown and returns JSON containing the processed HTML, title, tags, and cover image (if specified in front-matter).
6. The `Preview` component replaces the skeleton, rendering the article header (title, tags, cover image or video embed) and the full rendered body HTML.
7. Markdown accessibility lint runs in the background; any lint warnings appear in the preview header.

### Author toggles back to editing

1. While the preview panel is shown, the author clicks the "Edit" tab.
2. The editor dismisses the `Preview` component and restores the `Form` component, returning the author to the editing surface.
3. The `previewShowing` and `previewLoading` flags are both reset to false.

### Preview with cover image (v2 editor)

1. The author has uploaded a cover image, stored as `mainImage` in editor state.
2. On entering preview, the `Preview` component reads `articleState.mainImage` and renders it as the cover.
3. If the front-matter also specifies `cover_image`, that value from `previewResponse.cover_image` takes precedence when `previewShowing` is true.

### Preview with a video embed

1. The article has a `videoSourceUrl` set (YouTube, Mux, or Twitch URL) and no cover image.
2. In preview, the `Preview` component parses the URL into an embed URL and renders an `<iframe>` in the cover position with a 16:9 aspect ratio.

### Preview with validation errors

1. The markdown body contains content that causes the server's `ContentRenderer` to raise a `StandardError`.
2. The server returns 422 Unprocessable Entity with the error messages serialized as article errors.
3. The `Preview` component renders an `ErrorList` in the header area in place of the normal title/tag display.

## Failures / Exceptions

- If the author is not authenticated, `POST /articles/preview` returns 401 Unauthorized; the frontend `failedPreview` callback stores the error in state and clears the loading flag.
- If `ContentRenderer` raises a `StandardError`, the controller catches it, attaches the cleaned message to a transient `Article` object's errors, and renders 422 JSON; the editor displays the errors via `ErrorList`.
- If the fetch itself fails (network error), `failedPreview` is invoked and errors are stored in component state.
