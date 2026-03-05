---
id: "01KJ6FVWDXD1GEJNCWP4D2SAK0"
name: "system_assesses_article_quality_for_badge_criteria"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/ai/badge_criteria_assessor.rb`
- `spec/services/ai/badge_criteria_assessor_spec.rb` (Test)

## Functional Overview

`Ai::BadgeCriteriaAssessor` evaluates whether a given article qualifies for a badge award by delegating the decision to an AI model. The service builds a structured prompt that includes the article's title, publication date, tags, reading time, and up to the first 5,000 characters of its body. It appends the caller-supplied quality criteria and instructs the AI to respond with YES or NO. The AI's textual response is parsed case-insensitively: any response whose uppercased form contains "YES" is treated as a qualification. If the AI call raises any `StandardError`, the service logs the error and conservatively returns `false`, ensuring badge awards are never granted due to a technical failure.

## Design Intent

The fallback-to-false behavior on any `StandardError` is a deliberate safety measure. Badge awards should only be granted when there is a clear affirmative signal from the AI. Returning `false` on failure prevents erroneous badge grants caused by transient network errors, API quota exhaustion, or unexpected AI responses. The "contains YES" matching strategy (rather than an exact-match) adds tolerance for AI responses that embed the verdict inside a sentence while still guarding against false positives that contain "NO" but not "YES".

## Key Members

- `article` — the `Article` record to be evaluated; its `title`, `published_at`, `cached_tag_list`, `reading_time`, and `body_markdown` are included in the prompt.
- `criteria` — a caller-supplied string describing the quality standards the article must meet; injected at initialization and embedded verbatim in the prompt.

## Scenarios

### Article meets the quality criteria

1. A caller instantiates the assessor with an article and a criteria string.
2. The system constructs a prompt containing the article's metadata, its first 5,000 characters of content, and the criteria.
3. The system sends the prompt to the AI and receives a response containing "YES" (in any casing or as part of a sentence).
4. The system returns `true`, indicating the article qualifies.

### Article does not meet the quality criteria

1. A caller instantiates the assessor with an article and a criteria string.
2. The system sends the constructed prompt to the AI and receives a response of "NO".
3. The system finds no "YES" in the response and returns `false`.

### AI response is case-insensitive

1. The AI returns a lowercase or mixed-case affirmative such as "yes".
2. The system normalizes the response to uppercase before checking for "YES".
3. The system returns `true`.

### AI response embeds the verdict in a sentence

1. The AI returns a natural-language response such as "Based on my analysis, YES, this article qualifies."
2. The system checks whether the uppercased response contains "YES" anywhere.
3. The system returns `true`.

### AI call raises an error

1. The AI client raises a `StandardError` (e.g., due to a network failure or API error).
2. The system catches the exception and logs an error message prefixed with "Badge Criteria Assessment failed".
3. The system returns `false` without propagating the exception, preventing any badge from being granted due to a technical failure.

## Failures / Exceptions

- Any `StandardError` raised during the AI call is rescued. The error is logged via `Rails.logger.error` and the method returns `false` as a safe default.
- A `nil` AI response is handled gracefully: `parse_response` checks for `nil` before calling string methods, so a nil response returns `false`.
