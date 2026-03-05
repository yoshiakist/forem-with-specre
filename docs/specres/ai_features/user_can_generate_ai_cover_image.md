---
id: "01KJ6T0E5ZHZPXH2FM05E4X6Q6"
name: "user_can_generate_ai_cover_image"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/ai_image_generations_controller.rb`
- `app/policies/ai_image_generation_policy.rb`
- `app/services/ai/image_generator.rb`
- `spec/requests/ai_image_generations_spec.rb` (Test)
- `spec/services/ai/image_generator_spec.rb` (Test)

## Functional Overview

Authenticated, non-spam users can submit a text prompt to `POST /ai_image_generations` and receive a URL for an AI-generated cover image. The controller enforces per-user rate limiting before the request reaches the action, then uses Pundit to confirm the user is not flagged as spam. The user's prompt is enriched with subforem aesthetic instructions (looked up from the current subforem, falling back to the default subforem, then omitted if both are blank) and a fixed safety suffix that prohibits violent, lewd, or explicit content. An aspect ratio is derived from the subforem's cover image settings: in crop mode the ratio is calculated from a 1000-pixel-wide canvas divided by the configured height (capped at 500 px) and mapped to the nearest standard ratio; in limit mode the ratio is always `16:9`. The enriched prompt and ratio are passed to `Ai::ImageGenerator`, which calls the Gemini `gemini-2.5-flash-image` model via HTTP with a 30-second timeout enforced by the controller. On success the raw image data is decoded, written to a temporary file, uploaded through `ArticleImageUploader`, and the resulting URL is returned as JSON. The rate limiter counter is incremented only after a successful generation.

## Design Intent

Rate limiting is tracked on successful generations only so that failed or timed-out requests do not consume the user's quota. The height cap of 500 px prevents the system from requesting unusually tall (portrait) images that would look poor as cover art. The safety suffix is unconditional and appended last so it cannot be overridden by aesthetic instructions or user prompt content. Temporary files created during upload are always deleted in an `ensure` block to avoid disk leaks even when the upload raises an error.

## Key Members

- `GEMINI_IMAGE_MODEL` — `"gemini-2.5-flash-image"`, the Gemini model used for image generation.
- `VALID_ASPECT_RATIOS` — map of accepted ratio strings (e.g. `"16:9"`) to pixel dimensions; invalid ratios are rejected at construction time.
- `GenerationResult` — struct returned by `Ai::ImageGenerator#generate` carrying `url` and `text_response`.

## Scenarios

### Successful image generation

1. An authenticated, non-spam user posts a non-blank prompt to `POST /ai_image_generations`.
2. The rate limiter checks the user has not exceeded their quota; the Pundit policy confirms the user is not spam.
3. The controller fetches subforem aesthetic instructions and prepends them to the prompt, then unconditionally appends the safety suffix.
4. The aspect ratio is calculated from subforem cover image settings (crop mode) or defaults to `16:9` (limit mode).
5. `Ai::ImageGenerator` calls the Gemini API within a 30-second timeout, decodes the returned image, uploads it via `ArticleImageUploader`, and returns a `GenerationResult`.
6. The controller increments the rate limit counter and responds with `200 OK` and `{ url: "<uploaded_url>" }`.

### Prompt enriched with subforem aesthetic instructions

1. The subforem has non-blank aesthetic instructions configured.
2. The controller reads those instructions and combines them with the user prompt in the form: `"<prompt>. Style to use if not otherwise contradicted previously: <instructions>.\n\n<safety_suffix>"`.
3. The combined prompt is forwarded to the image generator unchanged.

### Aesthetic instructions fall back to default subforem

1. The current subforem has no aesthetic instructions set.
2. The controller checks whether a default subforem ID is present in the request store and fetches that subforem's aesthetic instructions instead.
3. The fallback instructions are combined with the prompt as above; if neither is set, only the safety suffix is appended.

### Aspect ratio derived from crop-mode cover image settings

1. The subforem's cover image fit mode is `"crop"`.
2. The controller computes a ratio from 1000 divided by the configured height (capped at 500); the floating-point result is mapped to the nearest standard ratio string (e.g. `"16:9"`, `"21:9"`, `"1:1"`).
3. The chosen ratio is passed to `Ai::ImageGenerator` and forwarded to the Gemini API.

### Rate limiting blocks excessive requests

1. A user submits enough successful generation requests to exhaust their quota.
2. On the next request the `limit_generations` before-action raises a rate-limit error before the action body executes.
3. The controller responds with `429 Too Many Requests`.

## Failures / Exceptions

- **Blank or missing prompt** — the controller returns `422 Unprocessable Entity` with `{ error: "..." }` before calling the generator.
- **Spam user** — Pundit raises `Pundit::NotAuthorizedError`; the policy's `create?` method returns `false` when `user.spam` is truthy.
- **Generation timeout** — a `Timeout::Error` after 30 seconds is rescued and returns `408 Request Timeout` with `{ error: "..." }`.
- **Generator returns nil** — when the Gemini API returns no image data or the upload fails, the generator returns `nil`; the controller responds with `422 Unprocessable Entity`.
- **Unexpected error** — any other `StandardError` is logged and returns `500 Internal Server Error` with `{ error: "..." }`.
- **Invalid aspect ratio** — `Ai::ImageGenerator` raises `ArgumentError` at construction if the ratio string is not in `VALID_ASPECT_RATIOS`.
- **Temporary file cleanup** — the `ensure` block in `upload_image` always closes and deletes the temp file, even when the upload raises an error.
