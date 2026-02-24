---
id: "01KJ6T4889WNMG34MDX8NHNQF3"
name: "system_enhances_article_metadata_via_ai"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/ai/article_enhancer.rb`
- `spec/services/ai/article_enhancer_spec.rb` (Test)

## Functional Overview

`Ai::ArticleEnhancer` enriches article metadata through two AI-powered capabilities: clickbait scoring and tag generation. Given an article and an optional injectable AI client, it can evaluate the article title against a 0.0–1.0 clickbait scale and auto-generate 2–4 relevant tags for articles that lack them. Tag generation uses a two-pass approach: a first AI call narrows up to 150 subforem candidate tags (ranked by hotness) down to a top-10 shortlist by name relevance, and a second call uses those tags' summaries to select the final 2–4. Both operations retry once on failure and fall back to safe defaults (0.0 and []).

## Design Intent

The two-pass tag selection reduces token usage: the first pass works only with tag names to cheaply cut the candidate pool, while the second pass loads richer tag summaries only for the shortlist. Keeping the AI client injectable (`ai_client:` keyword argument) makes the service straightforwardly testable without hitting the real API.

## Key Members

- `article` — the article whose metadata is being enhanced; title and first 750–1000 characters of body markdown are sent to the AI.
- `ai_client` — an `Ai::Base` instance used for all AI calls; defaults to a newly constructed instance but can be replaced via dependency injection.
- Candidate tags — up to 150 supported tags from the article's subforem, ordered by `hotness_score` descending.

## Scenarios

### Clickbait score for a normal title

1. Caller invokes `calculate_clickbait_score` on an `ArticleEnhancer` instance.
2. The system sends the article title to the AI with a scoring rubric that covers listicles, sensationalist phrasing, and ALL-CAPS headlines.
3. The AI returns a numeric string; the system parses the first numeric token and clamps it to the [0.0, 1.0] range.
4. The clamped float is returned to the caller.

### Clickbait score with out-of-range or non-numeric AI response

1. The AI returns a value outside [0.0, 1.0] or a non-numeric string.
2. Values above 1.0 are capped at 1.0; values below 0.0 are floored at 0.0; non-numeric responses yield 0.0.

### Tag generation via two-pass AI selection

1. Caller invokes `generate_tags` on an article that has no cached tag list.
2. The system fetches up to 150 supported tags for the article's subforem, ordered by hotness.
3. First AI pass: the system sends the article title and up to 1000 characters of body together with all candidate tag names; the AI returns the 10 most relevant names.
4. The system resolves those names back to tag records; if none match, an empty array is returned immediately.
5. Second AI pass: the system sends the article title and up to 750 characters of body together with the name and short summary of each shortlisted tag; the AI returns 2–4 final tag names as a comma-separated list, following guidance around `discuss`, `watercooler`, `career`, and `productivity` tags.
6. The final list of tag name strings is returned to the caller.

### Tag generation skipped when article already has tags

1. Caller invokes `generate_tags` on an article whose `cached_tag_list` is non-empty.
2. The system returns an empty array immediately without making any AI call.

### Retry and fallback on AI error

1. An AI call raises a `StandardError` (e.g., network or API error).
2. The system logs the failure and retries the entire operation once.
3. If the second attempt also fails, the system logs the final failure and returns the safe default: `0.0` for clickbait scoring or `[]` for tag generation.

## Failures / Exceptions

- Any `StandardError` raised during an AI call triggers one retry; after both attempts fail the method falls back to `0.0` (clickbait) or `[]` (tags) and logs error and info messages at each stage.
- If the candidate tag pool is empty (no supported tags in the subforem), `generate_tags` returns `[]` without calling the AI.
- If the first-pass AI response contains no names that match actual tag records, `generate_tags` returns `[]` without performing the second AI call.
- If the AI response to the final tag-selection pass indicates offensive, negative, or poorly written content, it is expected to return an empty string, which the system parses as `[]`.
