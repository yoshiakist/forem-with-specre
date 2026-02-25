---
id: "01KJ9R9MV7AYQY4YZP8F63RDVC"
name: "system_creates_mascot_account"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/services/users/create_mascot_account.rb`
- `spec/services/users/create_mascot_account_spec.rb` (Test)

## Functional Overview

`Users::CreateMascotAccount` is a service object that provisions a dedicated mascot user account for the Forem instance. When invoked, it checks whether a mascot account already exists by inspecting the `Settings::General.mascot_user_id` setting; if one is found, it raises an error to prevent duplicate provisioning. If no mascot exists, it creates a `User` record with fixed attributes (email, username, profile image, confirmation timestamp, registration timestamp, and a randomly generated password) along with an i18n-sourced display name, then stores the new user's ID in `Settings::General.mascot_user_id` for future reference.

## Design Intent

Using a frozen constant `MASCOT_PARAMS` for the fixed attributes makes the default mascot profile explicit and prevents accidental mutation. The guard that raises when `mascot_user_id` is already set enforces idempotency at the application layer — the service is intended to be called once per Forem instance, typically during initial setup or seeding.

## Key Members

- `MASCOT_PARAMS` — Frozen hash of fixed mascot attributes: `email`, `username`, `profile_image`, `confirmed_at`, `registered_at`, and a randomly generated `password`.
- `mascot_params` — Instance method that merges `MASCOT_PARAMS` with the i18n display name and a `password_confirmation` field before passing to `User.create!`.

## Scenarios

### Successfully creating the mascot account

1. The caller invokes the service (e.g., via `Users::CreateMascotAccount.call`).
2. The system checks `Settings::General.mascot_user_id`; the setting is blank, indicating no mascot exists yet.
3. The system creates a new User with the fixed mascot email, username, profile image, confirmed and registered timestamps, a randomly generated password, and the i18n-sourced display name.
4. The system stores the new user's ID in `Settings::General.mascot_user_id`.

### Attempting to create a mascot when one already exists

1. The caller invokes the service.
2. The system checks `Settings::General.mascot_user_id`; the setting already holds a user ID.
3. The system raises an error (using the `create_mascot.error` i18n key) and no new user is created.

## Failures / Exceptions

- If `Settings::General.mascot_user_id` is already set, the service raises a `RuntimeError` (via `I18n.t("create_mascot.error")`) before attempting to create any record.
- If `User.create!` fails validation, it raises `ActiveRecord::RecordInvalid` as normal ActiveRecord behavior.
