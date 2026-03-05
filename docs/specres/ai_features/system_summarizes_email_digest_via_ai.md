---
id: "01KJ6T999JZFEAT9S2K18TXENM"
name: "system_summarizes_email_digest_via_ai"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/ai/email_digest_summary.rb`
- `spec/services/ai/email_digest_summary_spec.rb` (Test)

## Functional Overview

`Ai::EmailDigestSummary` generates a short, thematic AI-powered overview for an email digest by sending a curated prompt to an AI client (defaulting to `Ai::Base`) and returning the response as a Markdown string. When called with a non-empty list of articles, it checks a Rails cache keyed by an order-independent MD5 hash of article paths (7-day expiry) and, on a cache miss, requests the AI to synthesise the articles into approximately two paragraphs using bold Markdown links — strictly no HTML. If the returned text contains raw HTML tags or malformed Markdown links, the service retries once with a stricter prompt addendum; after a second failure it logs the error and returns nil. Any unhandled exception from the AI client is also caught, logged, and causes the method to return nil.

## Design Intent

The cache key is derived from sorted article paths rather than IDs or order, making it resilient to article reordering and ensuring the same logical set of articles always hits the same cache entry. The output validation exists because LLMs occasionally slip HTML into their responses; a single retry with a reinforced no-HTML instruction resolves most such cases without making expensive multiple round-trips the norm. Returning nil on failure keeps callers safe — the email digest degrades gracefully by omitting the overview rather than crashing.

## Key Members

- `MAX_RETRIES = 1` — maximum number of times the service will re-prompt the AI after receiving invalid output before giving up and returning nil.
- `cache_key` — an MD5 digest of the sorted article paths, prefixed with `ai_digest_summary_v1_`, used as the Rails cache key for 7-day memoisation.

## Scenarios

### Successful summary generation

1. Caller instantiates `Ai::EmailDigestSummary` with one or more articles and optionally an AI client.
2. System checks the Rails cache using a key derived from the sorted article paths.
3. On a cache miss, system builds a prompt containing each article's title, URL, description, and tags, asking for a two-paragraph thematic synthesis using bold Markdown links and no HTML.
4. System sends the prompt to the AI client and receives a response.
5. System validates that the response contains no raw HTML tags and no malformed Markdown links.
6. Validation passes; system stores the result in the cache and returns the Markdown string to the caller.

### Cache hit returns stored result without calling the AI

1. Caller invokes `generate` a second time (or with a different ordering of the same articles).
2. System computes the same cache key (article paths are sorted before hashing, so order does not matter).
3. Cache entry exists and has not expired; system returns the cached Markdown string immediately without contacting the AI client.

### Retry on invalid AI output

1. AI client returns text that contains raw HTML tags or a malformed Markdown link.
2. System detects the violation in the output validator.
3. System logs a warning and appends a stricter no-HTML instruction to the original prompt.
4. System re-sends the augmented prompt to the AI client (this is attempt 2, the only allowed retry).
5. If the second response passes validation, system caches and returns it.
6. If the second response also fails validation, system logs an error and returns nil.

### Empty article list returns nil immediately

1. Caller invokes `generate` with an empty articles array.
2. System detects the empty input and returns nil without contacting the AI client or touching the cache.

### AI client exception returns nil and logs the error

1. AI client raises a `StandardError` (e.g., network failure or API error) during generation.
2. System rescues the exception, logs an error message containing the exception class and message, and returns nil to the caller.

## Failures / Exceptions

- **Empty articles:** `generate` returns nil immediately without any AI call or cache interaction.
- **Invalid markdown after max retries:** After one retry, if the output still contains HTML or malformed links, the service logs an error with a truncated sample of the bad output and returns nil.
- **AI client raises StandardError:** Any exception escaping from the AI client is caught at the `generate` level, logged, and converted to a nil return value so the caller is never exposed to an uncaught exception.
