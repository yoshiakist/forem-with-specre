---
id: "01KJ16TPFT4QGX88S3N5FMGKV5"
name: "system_labels_article_content_for_moderation"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/ai/content_moderation_labeler.rb`
- `spec/services/ai/content_moderation_labeler_spec.rb` (Test)

## Functional Overview

`Ai::ContentModerationLabeler` analyzes a submitted article and assigns it a structured content moderation label using an AI backend (`Ai::Base`). It builds a rich prompt that incorporates community context (drawn from `Settings::RateLimit` and `Settings::Community`, scoped to the article's subforem when present), the author's profile and activity statistics, and the article's title, tags, and body text (truncated to 5000 characters). The AI responds with a single label name from a fixed vocabulary covering safety, spam, quality, and relevance categories. If the AI call fails, the service retries up to two additional times before falling back to `"no_moderation_label"`. Invalid or unrecognized responses are also mapped to `"no_moderation_label"`.

## Design Intent

The retry-with-fallback pattern ensures that transient AI API errors do not block content processing: the system makes up to three total attempts, logging each failure and retry, and guarantees a safe default label rather than propagating an exception to callers. Separating prompt construction into private helpers (`build_prompt`, `build_user_context`, `build_article_context`) keeps the public `label` method focused on orchestration and error handling.

## Key Members

- `valid_labels` — A fixed allowlist of label strings that `parse_response` uses to validate AI output. Any response not in this list is normalized to `"no_moderation_label"`.

## Scenarios

### AI responds successfully on the first attempt

1. A caller instantiates `Ai::ContentModerationLabeler` with an article.
2. The service fetches community context from `Settings::RateLimit` or `Settings::Community` (subforem-scoped if the article has a `subforem_id`), assembles author statistics, and constructs a structured prompt.
3. The service calls `Ai::Base` with the prompt.
4. The AI returns a recognized label string (e.g., `"okay_and_on_topic"`).
5. `parse_response` strips, downcases, and validates the response against the allowlist, then returns the label.

### AI response is unrecognized or empty

1. The AI call succeeds but returns a value not present in the valid-labels allowlist, or returns a blank/nil response.
2. `parse_response` normalizes the response and finds no match in the allowlist.
3. The service returns `"no_moderation_label"`.

### AI call fails and all retries are exhausted

1. The AI call raises a `StandardError` on every attempt.
2. The service logs the failure and retries up to two more times (three total attempts), logging each retry.
3. After the third failure, the service logs a final error indicating fallback, and returns `"no_moderation_label"` without raising.

### AI call fails but succeeds on a subsequent retry

1. The AI call raises a `StandardError` on the first attempt (or subsequent attempts before the limit).
2. The service logs the failure and retries.
3. A later attempt succeeds and returns a recognized label.
4. The service returns that label without logging a fallback error.

## Failures / Exceptions

- Any `StandardError` raised by `Ai::Base#call` is rescued; the service retries up to two times and ultimately falls back to `"no_moderation_label"` rather than re-raising.
- A `nil` response from the AI is treated as an invalid response and mapped to `"no_moderation_label"`.
