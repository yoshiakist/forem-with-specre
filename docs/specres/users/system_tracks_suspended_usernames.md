---
id: "01KJBGNMW3FQS80A1NFAK9JPB4"
name: "system_tracks_suspended_usernames"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/models/users/suspended_username.rb`
- `spec/models/users/suspended_username_spec.rb` (Test)

## Functional Overview

The system maintains a persistent record of usernames that have previously been suspended or assigned a spam role. Rather than storing the raw username, it stores a SHA-256 hash of the username to enable privacy-preserving lookups. When a user is suspended or flagged as spam, their hashed username is recorded via `Users::SuspendedUsername`. The system can then query this record to determine whether a given username was previously associated with a suspended or spam account, preventing re-registration under the same name.

## Design Intent

Storing only the SHA-256 hash of the username rather than the plaintext ensures that the record cannot trivially reveal the original username, while still enabling exact-match lookups. Uniqueness is enforced at the database level via the `username_hash` column to prevent duplicate entries for the same username.

## Key Members

- `username_hash` — SHA-256 hex digest of the username; the sole persisted field; must be present and unique

## Scenarios

### Recording a suspended or spam user's username

1. An administrator suspends a user or assigns them the spam role
2. The system calls the convenience method with the user object
3. The system computes a SHA-256 hash of the user's username
4. A new `Users::SuspendedUsername` record is created in the database with that hash

### Checking whether a username was previously suspended

1. A username is submitted for lookup (e.g., during registration or role assignment)
2. The system computes the SHA-256 hash of the submitted username
3. The system queries the `users_suspended_usernames` table for a matching hash
4. If a matching record exists, the system reports that the username was previously suspended or flagged as spam
5. If no matching record exists, the system reports that the username has no suspension history

### Rejecting a duplicate suspended username record

1. An attempt is made to record a username hash that already exists in the table
2. The validation requires `username_hash` to be both present and unique
3. The record is rejected and an error is raised

## Failures / Exceptions

- Attempting to create a `Users::SuspendedUsername` without a `username_hash` raises a validation error (presence constraint)
- Attempting to create a duplicate entry for the same username hash raises a validation error (uniqueness constraint)
- `create_from_user` uses `create!` and will raise `ActiveRecord::RecordInvalid` if the record is invalid
