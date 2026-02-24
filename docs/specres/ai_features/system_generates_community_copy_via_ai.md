---
id: "01KJ6T87H9941SA2KXBV3E702M"
name: "system_generates_community_copy_via_ai"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/ai/community_copy.rb`
- `spec/services/ai/community_copy_spec.rb` (Test)

## Functional Overview

`Ai::CommunityCopy` generates three pieces of public and internal copy for a subforem by calling the Google Gemini API via `Ai::Base`. Given a subforem ID, a free-text brain dump, and an optional locale (default English), calling `write!` sequentially produces: a community description (50–200 chars), a tagline (10–50 chars), and an internal content-moderation specification (50–1500 chars). Each piece is generated independently with up to three retry attempts — retrying on API errors or on output that fails length validation — and is saved to the corresponding settings store only when a valid response is obtained. Raw AI responses are cleaned before validation to strip common conversational prefixes and suffixes. Failure of one piece does not abort the others, and all errors are logged rather than re-raised.

## Design Intent

Each copy type is kept independent so a transient API failure for one piece does not suppress the other two. The retry loop with a 1-second sleep between attempts guards against flaky upstream responses without blocking indefinitely. Length thresholds are relaxed in the test environment to allow short stub responses while maintaining meaningful minimums in production.

## Key Members

- `subforem_id` — identifies which subforem the generated copy belongs to; used as scope key when saving settings
- `brain_dump` — free-text input supplied by the operator that the AI uses as the primary source of context
- `locale` — language code (`'en'`, `'pt'`, `'fr'`); controls the language instruction injected into every prompt
- `MAX_RETRIES = 3` — maximum generation attempts per copy piece before giving up and logging an error

## Scenarios

### All three copy pieces generated successfully on first attempt

1. A caller instantiates the service with a subforem ID, a brain dump string, and an optional locale.
2. The system fetches community descriptions from other discoverable subforems to use as style references.
3. The system builds a prompt including the brain dump, reference examples, and a language instruction, then sends it to the AI.
4. The AI response is stripped of conversational prefixes and suffixes, then validated against the expected character-length range.
5. The cleaned description is saved via `Settings::Community.set_community_description` scoped to the subforem.
6. Steps 2–5 repeat for the tagline (using comparable taglines as references) and the internal content specification (no reference examples).
7. All three values are persisted and `write!` returns.

### AI response fails validation and the system retries

1. The AI returns a response that, after cleaning, falls outside the acceptable character-length range for the current copy type.
2. The system logs a warning identifying the attempt number and the copy type, resets the candidate value, and loops.
3. On a subsequent attempt the AI returns a response that passes validation; the system saves the value and continues.

### API call raises an error and the system retries with back-off

1. The AI API call raises a `StandardError` (e.g., network failure or non-2xx response).
2. The system increments the retry counter, logs a warning with the attempt number and error message, and sleeps one second before the next attempt.
3. If a later attempt succeeds, generation and saving proceed normally.

### All retry attempts exhausted for a copy piece

1. After three consecutive failures (validation failure or exception) for a given copy piece, the system logs an error stating that generation failed after the maximum number of attempts.
2. That copy piece is not saved; the remaining copy pieces continue to be generated independently.

### AI response contains conversational wrappers that must be stripped

1. The AI response begins with a phrase such as "Here is the description:" or ends with "Hope this helps!".
2. The system removes matching prefixes and suffixes via pattern substitution, then trims whitespace and trailing periods.
3. The cleaned string is passed to length validation; if it passes, it is saved as-is.

## Failures / Exceptions

- If a `StandardError` is raised during saving to `Settings::Community` or `Settings::RateLimit`, the error is caught, logged with context ("Failed to save community description: …"), and the remaining copy pieces continue to be processed.
- If `write!` itself raises an unexpected `StandardError` (outer rescue), the error is logged and the method returns without surfacing the exception to the caller.
- An API response that is blank, or that after cleaning still falls outside the length bounds, is treated as invalid and triggers a retry (not a hard error).
