---
id: "01KJBGYMQCJ8RJQV9SGE04C6TJ"
name: "system_prevents_banished_username_reuse"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/models/banished_user.rb`
- `app/models/user.rb`
- `spec/models/banished_user_spec.rb` (Test)

## Functional Overview

When a username is banished (recorded in the `BanishedUser` table), the system prevents any new or existing user from claiming that username again. The `BanishedUser` model normalizes usernames to lowercase before validation and enforces uniqueness within the banished list. The `User` model carries a custom validation that checks the banished list on every username change, adding a localized error message if a match is found. This two-model design keeps the banished-username registry separate from the active user table while still blocking reuse at the model layer.

## Scenarios

### Registering with a banished username is rejected

1. An administrator banishes a user, recording the lowercased username in the `BanishedUser` table.
2. A new visitor attempts to register with that same username (regardless of letter case).
3. The system normalizes the submitted username to lowercase and checks it against the banished list.
4. A match is found, so the system adds a validation error with the localized "has been banished" message.
5. Registration is rejected and the user is told the username is unavailable.

### Registering with a clean username succeeds

1. A visitor submits a username that does not appear in the `BanishedUser` table.
2. The system runs the banished-username check and finds no match.
3. No banishment error is added; other validations proceed normally.
4. Registration continues if all remaining validations pass.

### Each banished username entry is unique in the registry

1. An attempt is made to add the same username to the `BanishedUser` table a second time.
2. The model's uniqueness validation (scoped to `:create`) fires.
3. The duplicate entry is rejected, keeping the banished-username list free of redundant records.

## Failures / Exceptions

- If the submitted username is already present in the `BanishedUser` table, `User` validation adds the error key `models.user.has_been_banished` (resolved via I18n) to the `:username` attribute, causing the record to be invalid.
- The `BanishedUser` model rejects duplicate entries on create, preventing the same username from appearing in the banished list more than once.
