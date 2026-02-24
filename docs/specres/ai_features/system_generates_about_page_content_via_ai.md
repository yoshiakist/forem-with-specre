---
id: "01KJ6T4YYTJCCBGXEKWYZVX4J1"
name: "system_generates_about_page_content_via_ai"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/ai/about_page_generator.rb`
- `spec/services/ai/about_page_generator_spec.rb` (Test)

## Functional Overview

`Ai::AboutPageGenerator` accepts a subforem ID, a free-text brain dump, a community name, and an optional locale, then calls the Gemini API via `Ai::Base` to produce markdown About page content. The generator validates the response length (at least 200–5000 characters in production, at least 20 in test), strips AI meta-commentary and markdown code fences, and persists the result as a `Page` record with slug "about" and template "contained" — creating a new record or updating an existing one. If the AI call fails or produces content that does not meet expectations, the generator retries up to three times before logging an error and returning silently.

## Key Members

- `subforem_id` — identifies the subforem that owns the About page
- `brain_dump` — free-text description of the community provided by the caller; used verbatim in the AI prompt
- `name` — community display name; appears in the page title ("About {name}") and the prompt
- `locale` — BCP-47-style locale code; supported values are `en` (default), `pt` (Brazilian Portuguese), and `fr` (French)
- `MAX_RETRIES` (3) — maximum number of generation attempts before giving up

## Scenarios

### Successful first-attempt generation (new page)

1. The caller instantiates the generator with a valid subforem ID, a brain dump, a community name, and an optional locale.
2. The generator builds a prompt that includes the community name, brain dump, the subforem domain, locale-specific language requirements, and structural guidelines (welcoming intro, community purpose, encouraged content, participation guide, community guidelines; 300–800 words; markdown format; no AI preamble).
3. The generator calls `Ai::Base` with the prompt and receives a non-blank response.
4. The response is cleaned: leading AI prefixes ("Here is...", "I have generated...", etc.) and surrounding markdown code fences are stripped.
5. The cleaned content passes length validation (≥20 chars in test; 200–5000 chars in production).
6. Because no Page with slug "about" exists for this subforem, a new Page is created with title "About {name}", slug "about", `is_top_level_path: true`, and template "contained".

### Existing About page is updated

1. A Page record with slug "about" and the given subforem ID already exists.
2. After a successful AI generation and validation, the generator finds the existing page.
3. The existing page's title, description, and body markdown are updated with the newly generated content; no additional Page record is created.

### Retry on transient API failure

1. The AI call raises an error on the first attempt; the generator logs a warning and increments the retry counter.
2. If more retries remain, the generator waits one second and tries again.
3. On the third attempt the call succeeds and returns content that passes validation.
4. The About page is created or updated as normal.

### Retry on insufficient or oversized content

1. The AI call returns a response, but the content length does not meet the environment-specific threshold (too short in either environment, or too long in production).
2. The generator logs a warning, discards the response, and retries.
3. After exhausting all three attempts with insufficient content, the generator logs an error and returns without creating or modifying any Page.

### All attempts fail

1. Every AI call raises an error or every response fails validation across all three attempts.
2. The generator logs a final error message ("Failed to generate about content after 3 attempts") and returns without raising; no Page record is created or modified.

## Failures / Exceptions

- Any `StandardError` raised inside `generate_about_page_with_retry` (including from `create_about_page`) is rescued, logged at error level, and swallowed — the caller receives `nil` rather than an exception.
- If the AI response is blank or `nil`, `parse_about_response` returns `nil`, which causes the validation check to treat the attempt as failed and trigger a retry.
