---
id: "01KJ1CEX2PVN8VG917WAMM06V4"
name: "author_can_generate_ai_cover_image"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/javascript/article-form/components/ArticleCoverImage.jsx` (AiImagePromptModal component; AI-related state and handlers in ArticleCoverImage)
- `app/javascript/article-form/actions.js` (generateAiImage function)

## Functional Overview

When the Forem instance has AI image generation enabled (`aiAvailable` prop is true), the article editor presents a "Generate Image" button alongside the standard cover image upload controls. Clicking this button opens a modal (`AiImagePromptModal`) where the author types a freeform text description of the desired image. On submission, the prompt is sent to the `/ai_image_generations` endpoint via a POST request. If the server returns a URL, it is applied as the article's cover image and a success snackbar is shown. While generation is in progress the modal locks — the close button and cancel action are hidden and the form fields are disabled — preventing the author from accidentally dismissing the operation. Errors returned by the server or triggered by a client-side 35-second timeout surface inline below the image upload controls.

## Design Intent

The modal locks during generation (hiding close and cancel controls) to prevent the author from dismissing the request mid-flight, which would leave the server doing work with no consumer for the result. The client-side 35-second timeout is set slightly longer than the expected server timeout so the client always surfaces a user-friendly message rather than receiving a raw HTML error page or a stale response.

## Key Members

- `showAiPrompt: boolean` — controls visibility of the `AiImagePromptModal`; set to true when the author clicks "Generate Image", false after a successful generation or explicit dismiss
- `generatingAiImage: boolean` — true while the `/ai_image_generations` request is in-flight; gates the modal's close affordance and the form's interactivity
- `prompt: string` (local to `AiImagePromptModal`) — the text description the author types; form submission is blocked when this is empty or whitespace-only
- `generateAiImage({ prompt, successCb, failureCb, signal })` — issues the POST request and manages the 35-second client-side timeout

## Scenarios

### Author opens the AI generation modal

1. The article editor renders with `aiAvailable` set to true and no existing cover image.
2. A "Generate Image" button is visible in the cover image controls area.
3. Author clicks the button.
4. The `AiImagePromptModal` appears with a textarea for the image description, a disabled "Generate Image" submit button, and a "Cancel" button.

### Author submits a valid prompt and generation succeeds

1. The modal is open and the author types a non-empty description into the prompt textarea.
2. The submit button becomes enabled.
3. Author clicks "Generate Image".
4. The modal enters a generating state: the submit button shows a spinner and "Generating..." label, the textarea is disabled, and the close/cancel affordances are hidden.
5. The client sends a POST to `/ai_image_generations` with the prompt as JSON.
6. The server responds with a JSON body containing a `url` field.
7. The modal closes, the returned URL is set as the article's cover image, and a success snackbar message appears.

### Author submits a valid prompt and generation fails

1. The modal is open, the author enters a prompt, and clicks "Generate Image".
2. The server responds with a non-2xx status or a JSON body containing an `error` field, or the client-side 35-second timeout fires.
3. The generating state ends; the modal remains open.
4. An error message is displayed below the cover image controls indicating the failure reason (or a generic fallback if the response is an HTML error page).

### Author dismisses the modal without generating

1. The modal is open and no generation is in progress.
2. Author clicks "Cancel" or the close button.
3. The modal closes and any prior error state is cleared.

### Author cannot close the modal while generation is in progress

1. The author has submitted a prompt and the request is in-flight.
2. The close button and "Cancel" button are not rendered in the modal.
3. The modal remains visible until the generation completes or fails.

## Failures / Exceptions

- If the server returns a non-2xx HTTP status, the response body is not parsed; a generic error message "An error occurred, please try again later" is surfaced instead of potentially leaking HTML content.
- If the server returns a JSON body with an `error` key, that error message is shown to the author.
- If generation takes longer than 35 seconds (client-side timeout), a "Image generation timed out. Please try again." message is shown. This only fires if the request has not already been aborted via the optional `signal`.
- If the prompt is empty or contains only whitespace, form submission is blocked at the client; the submit button remains disabled.
