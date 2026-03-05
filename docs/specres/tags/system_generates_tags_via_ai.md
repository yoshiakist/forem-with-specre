---
id: "01KJ41N4Q80SANVK8KV9VEDB88"
name: "system_generates_tags_via_ai"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/ai/forem_tags.rb`
- `spec/services/ai/forem_tags_spec.rb` (Test)

## Functional Overview

`Ai::ForemTags` generates a curated set of tags for a subforem by sending a structured prompt to an AI service (`Ai::Base`), parsing the line-delimited response into validated tag name/description pairs, and upserting each tag into the database. The service targets 60 tags per run, retries generation up to 3 times when the output is insufficient, enforces a strict alphanumeric-only format for tag names, and links each accepted tag to the subforem via a `TagSubforemRelationship`. When a conflicting tag name already exists, the service uses AI-assisted semantic similarity comparison (with a word-overlap fallback) to decide whether to skip the tag or generate a uniquely suffixed name. The locale parameter controls the language of both the tag generation prompt and the resulting descriptions.

## Design Intent

The retry loop guards against transient AI API failures and low-quality responses without blocking the caller; `upsert!` swallows all errors at the top level so a single failure does not interrupt background jobs. AI similarity comparison is used as the primary deduplication strategy with a deterministic word-overlap fallback to ensure resilience when the AI call itself fails.

## Key Members

- `MAX_RETRIES = 3` — maximum number of generation attempts before giving up
- `TARGET_TAG_COUNT = 60` — desired number of tags per generation run
- `@subforem_id` — identifies which subforem the generated tags belong to
- `@brain_dump` — free-text description of the community, used as context in the AI prompt
- `@locale` — language code (`'en'`, `'pt'`, `'fr'`) controlling prompt language instructions

## Scenarios

### Successful tag generation and creation

1. Caller invokes `upsert!` with a subforem ID, a community description, and an optional locale.
2. The service builds a prompt requesting 60 tags in `name: description` format, including a locale-appropriate language instruction.
3. The prompt is sent to `Ai::Base`; the response is split by newlines and each line is parsed into a name/description pair.
4. Lines with invalid tag names (containing special characters, pure numbers, fewer than 2 or more than 50 characters) are discarded.
5. Valid tags are processed one by one: new tags are created as `Tag` records with `supported: true` and linked to the subforem via `TagSubforemRelationship`.

### Generation retry on failure or insufficient output

1. The AI call raises an error or returns fewer valid tags than 80% of the target count.
2. The service logs a warning and increments a retry counter; if retries remain it sleeps briefly and tries again.
3. After 3 failed attempts the service logs an error and returns without persisting any tags.

### Existing tag without a subforem relationship

1. A generated tag name matches an existing `Tag` record that has no `TagSubforemRelationship` for the current subforem.
2. If the existing tag has no description, the service sets its `short_summary` to the AI-generated description.
3. A new `TagSubforemRelationship` is created to link the existing tag to the subforem.

### Existing tag with relationship and similar meaning

1. A generated tag name matches an existing `Tag` that already has a `TagSubforemRelationship` for the subforem.
2. The service calls `Ai::Base` with a comparison prompt to determine whether the existing and new descriptions are semantically similar.
3. If the AI responds with "YES" or "similar", the tag is skipped and a log message is recorded.
4. If the AI call fails, the service falls back to a word-overlap ratio check (threshold: 30%).

### Existing tag with relationship but different meaning

1. A generated tag name matches an existing `Tag` with a subforem relationship, but the AI (or fallback) determines the descriptions differ in meaning.
2. The service generates a unique name by appending an incrementing numeric suffix (e.g., `webdev1`, `webdev2`) until a non-colliding name is found.
3. A new `Tag` with the suffixed name and AI-generated description is created and linked to the subforem.

## Failures / Exceptions

- `ActiveRecord::RecordInvalid` during tag creation is caught per-tag; the error is logged and processing continues with remaining tags.
- `ActiveRecord::RecordInvalid` during relationship creation is caught per-relationship; the tag record is left without a relationship and processing continues.
- Any `StandardError` raised during the entire `process_tags` iteration is caught and logged without re-raising.
- Any unhandled error from `generate_tags_with_retry` is caught by `upsert!` and logged, preventing caller disruption.
