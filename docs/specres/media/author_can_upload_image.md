---
id: "01KJ1C8G3AN3EVK907SGXDWZG5"
name: "author_can_upload_image"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/image_uploads_controller.rb`
- `app/controllers/concerns/image_uploads.rb`
- `app/javascript/article-form/components/ArticleCoverImage.jsx`
- `app/javascript/article-form/components/ImageUploader.jsx`
- `app/javascript/article-form/actions.js`
- `app/javascript/packs/validateFileInputs.js`
- `app/javascript/article-form/components/dragAndDropHelpers.js`
- `app/javascript/article-form/components/ClipboardButton.jsx`
- `spec/requests/image_uploads_spec.rb` (Test)
- `app/javascript/article-form/components/__tests__/ArticleCoverImage.test.jsx` (Test)
- `app/javascript/article-form/components/__tests__/ImageUploader.test.jsx` (Test)
- `app/javascript/article-form/components/__tests__/dragAndDropHelpers.test.js` (Test)

## Functional Overview

Authenticated authors can upload images to attach to articles through two distinct entry points: the cover image slot (`ArticleCoverImage`) and the inline markdown editor toolbar (`ImageUploader`). Both entry points perform client-side validation (file type must be `image/*`, size must not exceed 25 MB, filename must not exceed 250 characters) before posting to `POST /image_uploads` via `generateMainImage`. The backend (`ImageUploadsController`) enforces authorization, re-validates that the upload is a real file with an acceptable filename length, delegates storage to `ArticleImageUploader`, and returns a JSON array of CDN URLs. The cover image entry point additionally supports drag-and-drop of a single image and a native iOS bridge path (`ForemMobile` `coverUpload` namespace). The inline editor entry point (`ImageUploader`) supports both v1 and v2 editor layouts, an abort/cancel flow for in-flight uploads, and exposes the resulting markdown image snippet via a clipboard copy button (`ClipboardButton`). Upload rate limiting is enforced server-side, returning HTTP 429 with a `Retry-After` header when the limit is exceeded.

## Design Intent

Client-side validation via `validateFileInputs` runs before any network request, providing immediate feedback and avoiding unnecessary server round-trips. The backend re-validates independently (`ImageUploads` concern) so the two layers act as independent guards rather than trusting the client. The native iOS code path uses a `ForemMobile` `CustomEvent` bridge rather than a standard file input, keeping web and native behaviors isolated while sharing the same state-handling logic. The v2 editor wraps each upload in an `AbortController` so authors can cancel a slow upload mid-flight without leaving the UI in a stuck state.

## Key Members

- `generateMainImage({ payload, successCb, failureCb, signal })` — posts a `FormData` request to `POST /image_uploads`; `signal` carries the optional `AbortController` signal for cancellation
- `processImageUpload(images, handleImageUploading, handleImageSuccess, handleImageFailure)` — thin orchestration helper used by the drag-and-drop path; calls `validateFileInputs` then `generateMainImage`
- `MAX_FILE_SIZE_MB` — `{ image: 25, video: 50 }` default limits applied during client-side validation
- `MAX_FILE_NAME_LENGTH` — 250 characters, enforced both client-side and server-side
- `imageUploaderReducer` — manages `uploadingImage`, `uploadErrorMessage`, and `insertionImageUrls` state in `ImageUploader`

## Scenarios

### Cover image upload via file picker (web)

1. The author clicks "Upload Cover Image" (or "Change") in the article form header, which opens the native file picker filtered to `image/*`.
2. On file selection the component calls `validateFileInputs`, which checks size (25 MB max), MIME type (must be `image`), and filename length (250 chars max); any violation is shown as a snackbar error and the upload is aborted.
3. If client validation passes, the component sets the uploading state, packages the file into `FormData`, and sends `POST /image_uploads` with the CSRF token.
4. The backend authenticates the user, checks rate limits, re-validates file type and filename length, stores the file with `ArticleImageUploader`, and returns `{ links: [url] }`.
5. On success the parent receives the URL via `onMainImageUrlChange`; on failure the error message is displayed inline below the upload controls.

### Cover image upload via drag and drop

1. The author drags an image file over the `DragAndDropZone` in the article cover area; the zone gains the `drop-area--active` CSS class.
2. On drop, if more than one file is present the action is rejected with a snackbar message "Only one image can be dropped at a time." and no upload occurs.
3. If exactly one file is dropped, `handleMainImageUpload` is called, which proceeds identically to the file-picker flow (client validation → `POST /image_uploads` → success/failure handling).

### Inline image upload in the v2 editor toolbar

1. The author clicks the image icon in the v2 editor toolbar, triggering a click on the visually hidden file input (`#image-upload-field`).
2. File selection invokes `handleInsertionImageUpload`, which validates inputs and dispatches `uploading_image`; the toolbar button switches to a cancel/spinner state.
3. The author may click the cancel button at any time, which calls `AbortController.abort()` to cancel the in-flight request; the toolbar returns to the upload-ready state.
4. On successful upload the response links are inserted into the editor body as `![Image description](<url>)` markdown via `onImageUploadSuccess`, and an accessible live region announces "image upload complete".
5. On failure a snackbar error message is displayed via the `upload_error` reducer action.

### Inline image upload in the v1 editor

1. The author clicks "Upload image" in the v1 editor upload panel, selecting a file from the picker (multiple files allowed by the input).
2. Client validation runs; passing files trigger a `generateMainImage` call and the uploading spinner appears.
3. On success, the returned URLs are placed in a read-only text field as comma-joined `![Image description](<url>)` markdown and a `ClipboardButton` appears so the author can copy the snippet.
4. On failure an inline error span is shown within the upload panel.

### Native iOS cover image upload

1. On the Forem iOS native app, the cover image button dispatches an `injectNativeMessage('coverUpload', { action: 'coverImageUpload', ... })` call to the native layer instead of opening a file picker.
2. The native layer emits `ForemMobile` custom events with `namespace: 'coverUpload'` and `action` values of `uploading`, `success`, or `error`.
3. The component handles each action: `uploading` sets the spinner, `success` calls `onMainImageUrlChange` with the link, and `error` displays the error message inline.

## Failures / Exceptions

- **Unauthenticated request**: `POST /image_uploads` returns HTTP 401.
- **Missing or non-file parameter**: the backend returns HTTP 422 with `{ error: "..." }` (message from `is_not_file_message`).
- **Filename too long (>250 chars)**: HTTP 422 with `{ error: "..." }` (message from `filename_too_long_message`).
- **CarrierWave::IntegrityError** (e.g., image resolution exceeds 4096×4096): HTTP 422 with `{ error: e.message }`.
- **CarrierWave::ProcessingError**: HTTP 422 with a generic server error message from `i18n`.
- **Rate limit exceeded**: HTTP 429 with a `Retry-After` header set to the configured retry interval; enforced after 10 uploads within the window.
- **Client-side size/type/name violation**: upload is blocked before the request is sent; a snackbar error is shown to the author.
- **Multiple files dropped on cover zone**: upload is rejected with a snackbar "Only one image can be dropped at a time."
