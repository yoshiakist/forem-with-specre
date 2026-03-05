---
id: "01KJ9JE1SPDCRJXAB1S3R7EKGT"
name: "system_records_user_language_preference"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/models/user_language.rb`
- `spec/models/user_language_spec.rb` (Test)
- `spec/factories/user_languages.rb` (Test)

## Functional Overview

`UserLanguage` is an ActiveRecord model that records a single language preference for a user. Each record belongs to a user and stores a language code. The model enforces that the language code is present and must appear in the list of codes recognized by `Languages::Detection`, ensuring only valid, known language codes are persisted.

## Scenarios

### Recording a valid language preference

1. A user language record is created with a user reference and a valid language code recognized by `Languages::Detection`.
2. The record passes validation and is saved successfully.

### Rejecting a missing language code

1. A user language record is created without a language code.
2. The system rejects the record and reports a presence validation error on the `language` field.

### Rejecting an unrecognized language code

1. A user language record is created with a language code that does not appear in `Languages::Detection.codes`.
2. The system rejects the record and reports an inclusion validation error on the `language` field.

## Failures / Exceptions

- If `language` is blank, a presence error is added to the `language` attribute and the record is not saved.
- If `language` is not included in `Languages::Detection.codes`, an inclusion error is added to the `language` attribute and the record is not saved.
