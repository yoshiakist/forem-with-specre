---
id: "01KJA2E4NR5V43929VH74R957F"
name: "system_detects_user_language_from_visit_context"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/models/user_visit_context.rb`
- `spec/models/user_visit_context_spec.rb` (Test)
- `spec/factories/user_visit_contexts.rb` (Test)

## Functional Overview

When a new `UserVisitContext` record is created, the system automatically parses the visitor's `Accept-Language` HTTP header and creates `UserLanguage` records for any language codes with a quality weight of 0.7 or higher. Language codes are normalized to their two-character prefix (e.g., `en-US` becomes `en`), deduplicated by language code, and upserted idempotently using `first_or_create`. This ensures that a user's preferred languages are recorded at the time of their first detected visit in a given context, without creating duplicate entries.

## Design Intent

The threshold of 0.7 filters out low-preference languages that browsers list as fallbacks, keeping only languages the user genuinely prefers. The `after_create` callback ensures language detection is automatic and does not require callers to invoke it explicitly. Errors are caught and logged rather than propagated, preventing visit context creation from failing due to language detection issues.

## Key Members

- `accept_language` — raw `Accept-Language` header string stored on the record, e.g. `"en-US;q=0.9,fr-FR;q=0.8"`
- `user_id` — foreign key linking the visit context to its owner, used when creating `UserLanguage` records

## Scenarios

### Languages above quality threshold are recorded

1. A new `UserVisitContext` is saved with an `accept_language` header listing one or more languages with quality values.
2. After the record is created, the system splits the header into individual language entries.
3. Each entry is parsed for its two-character language code and optional quality weight (defaulting to `1.0` when absent).
4. Only entries with a quality weight of 0.7 or greater are retained.
5. Duplicate language codes are removed, keeping only the first occurrence of each code.
6. A `UserLanguage` record is found or created for each remaining language code scoped to the user.

### Language code is normalized to two characters

1. A language tag such as `en-US` or `fr-FR` is present in the header.
2. The system extracts only the first two characters of the tag as the language code.
3. The resulting code (`en`, `fr`) is used when creating the `UserLanguage` record.

### Quality weight defaults to 1.0 when omitted

1. A language entry in the header has no explicit `;q=` qualifier (e.g., the first listed language).
2. The system treats its quality weight as `1.0`, which exceeds the 0.7 threshold.
3. The language is included in the set to be recorded.

### Languages below quality threshold are ignored

1. A language entry carries a quality weight below 0.7 (e.g., `;q=0.5`).
2. The system filters it out during selection.
3. No `UserLanguage` record is created for that language code.

## Failures / Exceptions

- If any error occurs during language detection (e.g., a database error while creating `UserLanguage`), the exception is rescued and logged via `Rails.logger.error`. The `UserVisitContext` record itself is unaffected and the callback completes silently.
