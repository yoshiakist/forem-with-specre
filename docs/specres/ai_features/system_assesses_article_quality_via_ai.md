---
id: "01KJ6T4NE3KFCGASC42XB50SKP"
name: "system_assesses_article_quality_via_ai"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/ai/article_quality_assessor.rb`
- `spec/services/ai/article_quality_assessor_spec.rb` (Test)

## Functional Overview

`Ai::ArticleQualityAssessor` compares a set of articles using an AI language model to identify the highest-quality and lowest-quality entries. It is intended only for nudging purposes and must not be used for major moderation actions. The assessor builds a structured prompt that embeds community context (drawn from either an internal content-description spec or the community description setting, optionally scoped to a subforem), article metadata (tags, title, body truncated to 10,000 characters, and up to three top comments), and detailed qualitative criteria. The AI is expected to respond with two 1-based article indices; these are parsed and converted into the corresponding article objects returned as `{ best:, worst: }`. When the response is absent, malformed, or out of range, or when the AI call raises an error, the method falls back to `{ best: nil, worst: nil }`. Two degenerate cases are handled before any AI call: an empty article list returns `{ best: nil, worst: nil }`, and a single-article list returns that article for both keys.

## Design Intent

The behavior is deliberately non-authoritative — fallback always returns `nil` rather than a heuristic selection — to prevent incorrect AI output from triggering meaningful platform actions. Community context is injected into every prompt so that quality judgment is relative to each community's stated purpose, not an absolute standard.

## Key Members

- `articles` — the array of `Article` objects to compare; order matters because AI response indices are 1-based positions in this array.
- `subforem_id` — optional integer that scopes the community-context lookup to a specific subforem.
- `assess` — public method; returns `{ best: Article | nil, worst: Article | nil }`.

## Scenarios

### Empty article list

1. Caller passes an empty array to `Ai::ArticleQualityAssessor`.
2. The assessor immediately returns `{ best: nil, worst: nil }` without calling the AI.

### Single article

1. Caller passes an array containing exactly one article.
2. The assessor returns `{ best: <that article>, worst: <that article> }` without calling the AI.

### Successful multi-article assessment

1. Caller passes two or more articles, optionally with a `subforem_id`.
2. The assessor fetches the community context: if `subforem_id` is given, it tries the subforem-scoped internal content description spec first, then the subforem-scoped community description; otherwise it uses the global equivalents.
3. A prompt is built that lists each article with its tags, title, truncated body, and top three comments (if any), followed by the assessment criteria and a request for two comma-separated 1-based indices.
4. The AI client is called with this prompt and returns a string such as `"3,1"`.
5. The assessor extracts the first two integers, validates they are within range, and returns `{ best: articles[first-1], worst: articles[second-1] }`.

### Malformed or out-of-range AI response

1. The AI returns a response that contains fewer than two integers, or indices that fall outside the valid range for the article array.
2. The assessor calls `fallback_assessment` and returns `{ best: nil, worst: nil }`.

### AI call raises an error

1. The AI client raises a `StandardError` during the call (e.g., network failure, API error).
2. The error is logged via `Rails.logger.error`.
3. The assessor returns `{ best: nil, worst: nil }`.

## Failures / Exceptions

- Any `StandardError` raised by the AI client is rescued; the error message is logged and `{ best: nil, worst: nil }` is returned.
- A response with no parseable integers, or with valid integers that do not correspond to valid article positions, is treated as a failure and falls back to `{ best: nil, worst: nil }`.
