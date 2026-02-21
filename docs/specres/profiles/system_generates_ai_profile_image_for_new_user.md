---
id: "01KHZ6KPVGP495ZDNG16MKD6FK"
name: "system_generates_ai_profile_image_for_new_user"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/workers/users/generate_ai_profile_image_worker.rb`
- `spec/workers/users/generate_ai_profile_image_worker_spec.rb` (Test)

## Functional Overview

When a new user is created, the system enqueues a background job (`Users::GenerateAiProfileImageWorker`) that generates an AI-produced profile image via `Ai::ImageGenerator`. The job builds a prompt based on a fixed sloth mascot description, optionally augmented with site-level or subforem-level aesthetic instructions fetched from `Settings::UserExperience`. If generation succeeds and returns a URL, the user's `remote_profile_image_url` is updated and saved. Any unhandled error during this process is logged and reported to Honeybadger, preventing the failure from surfacing to the end user.

## Design Intent

The prompt always includes a content safety suffix (`CONTENT_SAFETY_SUFFIX`) appended unconditionally to prevent the AI from generating violent, explicit, or inappropriate content regardless of any prior instructions. Aesthetic instructions are layered on top of the base prompt rather than replacing it, ensuring the sloth mascot identity is preserved while allowing per-site customization.

## Key Members

- `MAGIC_LINK_PLACEHOLDER_PROMPT` — Fixed base prompt describing a friendly sloth mascot portrait in an illustrated style.
- `CONTENT_SAFETY_SUFFIX` — Appended to every prompt to enforce content safety constraints.
- `sidekiq_options queue: :low_priority, retry: 5` — Job runs on the low-priority queue and retries up to 5 times on transient failures.

## Scenarios

### User is not found

1. The job receives a `user_id` that does not correspond to any existing user.
2. The system looks up the user and, finding none, exits immediately without contacting the image generator.

### Image generation succeeds without aesthetic instructions

1. The job receives a valid `user_id` and loads the corresponding user record.
2. No global or subforem aesthetic instructions are configured.
3. The system builds a prompt from `MAGIC_LINK_PLACEHOLDER_PROMPT` with the content safety suffix appended.
4. `Ai::ImageGenerator` is called with this prompt and returns a result containing an image URL.
5. The user's profile image is updated to that URL and the record is saved.

### Image generation succeeds with global aesthetic instructions

1. The job receives a valid `user_id` and loads the user record.
2. Global aesthetic instructions are configured in `Settings::UserExperience`.
3. The system builds an augmented prompt that incorporates those instructions after the base sloth description, followed by the content safety suffix.
4. `Ai::ImageGenerator` is called with the augmented prompt and returns a URL.
5. The user's profile image is updated and saved.

### Image generation succeeds with subforem aesthetic instructions

1. The job receives a valid `user_id` and loads the user record.
2. No global aesthetic instructions are set, but a `default_subforem_id` is present in the request store and subforem-specific instructions exist.
3. The system fetches those subforem instructions and builds an augmented prompt.
4. `Ai::ImageGenerator` returns a URL and the user's profile image is updated and saved.

### Image generation returns no URL

1. The job receives a valid `user_id` and loads the user record.
2. `Ai::ImageGenerator` is called but returns a nil result or a result without a URL.
3. The system exits without updating the user's profile image.

## Failures / Exceptions

- If any `StandardError` is raised during generation or saving, the error message is written to the Rails log and the exception is reported to Honeybadger (when available) with the `user_id` as context. The job does not re-raise, so Sidekiq's automatic retry mechanism governs subsequent attempts up to the configured limit of 5.
