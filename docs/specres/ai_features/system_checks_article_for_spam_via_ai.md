---
id: "01KJ6T0FTCFV8J7DD5NS206RSK"
name: "system_checks_article_for_spam_via_ai"
status: "draft"
---

## Related Files

- `app/services/ai/article_check.rb`

## Functional Overview

`Ai::ArticleCheck` uses a Google Gemini AI model to determine whether a given article is spam. When `spam?` is called, it assembles a rich prompt that includes the community's content description or community description, the author's ten most recent article titles as a behavioral pattern, and the article's own title and body. The assembled prompt asks the AI to respond with a single word — YES or NO — and the service treats a stripped, uppercased "YES" response as spam. Any exception raised during the AI call is rescued and causes the check to return false, preserving a fail-open default that favors user experience over false positives.

## Design Intent

Fail-open on error means a transient API failure or malformed response never incorrectly blocks a legitimate article. The design targets only clear spam rather than borderline cases, intentionally accepting some false negatives in exchange for avoiding false positives that would harm genuine contributors.

## Key Members

- `article` — the article being evaluated; must expose `title`, `body_markdown`, `user`, and `subforem_id`
- `spam?` — the single public method; returns `true` if the AI says YES, `false` otherwise

## Scenarios

### Article is clearly spam

1. Caller instantiates `Ai::ArticleCheck` with an article object.
2. The service fetches the author's ten most recent article titles and the community description for the article's subforem.
3. A prompt is assembled combining community context, author history, and the article title and body, instructing the AI to answer YES or NO.
4. The AI responds with "YES".
5. `spam?` returns `true`.

### Article is not spam

1. Caller instantiates `Ai::ArticleCheck` with an article object.
2. The service builds the prompt with community context, author history, and article content.
3. The AI responds with "NO" (or any text other than the exact word "YES" after stripping and uppercasing).
4. `spam?` returns `false`.

### Community context is available

1. The service looks up `Settings::RateLimit.internal_content_description_spec` for the article's subforem.
2. If a value is present, it is used as the community context in the prompt.
3. If absent, `Settings::Community.community_description` is used as a fallback.
4. If neither is set, the prompt notes "No community description provided."

### Author has no article history

1. The article's author has published no previous articles.
2. The service finds an empty history list.
3. The prompt records "No article history available." in the author history section.
4. Spam detection proceeds normally with only community context and the article itself.

### AI call raises an error

1. The AI client raises any `StandardError` (network failure, malformed response, API error, etc.).
2. The error is logged via `Rails.logger.error`.
3. `spam?` returns `false` without re-raising, preserving normal article publication flow.

## Failures / Exceptions

- Any `StandardError` from the AI call is rescued; the method logs the error and returns `false` (fail-open).
- A nil or non-"YES" AI response is treated as not spam; the parse step does not raise.
