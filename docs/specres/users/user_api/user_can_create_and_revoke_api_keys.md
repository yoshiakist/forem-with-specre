---
id: "01KJ9MTNQVSA7QWHW4VYYX71M4"
name: "user_can_create_and_revoke_api_keys"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/api_secrets_controller.rb`
- `app/policies/api_secret_policy.rb`
- `app/views/users/_api_keys.html.erb` (Template)
- `spec/requests/api_secrets_create_spec.rb` (Test)
- `spec/requests/api_secrets_destroy_spec.rb` (Test)
- `spec/models/api_secret_spec.rb` (Test)
- `spec/policies/api_secret_policy_spec.rb` (Test)

## Functional Overview

Authenticated users can generate personal API keys (called `ApiSecret` records) with a description, and later revoke any of their own keys. Key creation is handled via a POST to `users/api_secrets`, which builds the record with the current user's identity, saves it, and flashes the generated secret token in a notice so the user can copy it immediately. Revocation is handled via a DELETE to `users/api_secrets/:id`, which loads the record and destroys it. Both actions are protected by Pundit policy: only the owning user may delete a key, and suspended or spam-flagged users may not create new keys. After each action the user is redirected back to the previous page.

## Design Intent

The generated secret token is exposed exactly once — in the flash notice immediately after creation — so it is never stored in a retrievable form in the UI. Pundit authorization enforces ownership on destroy so one user can never revoke another user's key. The redirect-back pattern keeps the flow contained within the settings page without requiring a dedicated response view.

## Key Members

- `ApiSecret#description` — human-readable label required on creation (max 300 characters)
- `ApiSecret#secret` — the generated token, surfaced once in the flash notice after creation
- Per-user limit of 10 active API keys enforced at the model level

## Scenarios

### User generates a new API key

1. An authenticated user navigates to the Extensions settings page, which renders the API keys partial.
2. The user enters a description in the "Generate API key" form and submits it.
3. The system creates an `ApiSecret` record associated with the current user.
4. The generated secret token is displayed once in a flash notice; no error message appears.
5. The user is redirected back to the settings page.

### Key creation fails due to validation error

1. An authenticated user submits the API key form without a description (or with an invalid value).
2. The `ApiSecret` record fails validation and is not saved.
3. A flash error message is shown; no notice message appears.
4. The user is redirected back to the settings page.

### User revokes an existing API key

1. An authenticated user views their list of active API keys on the settings page.
2. The user clicks the "Revoke" button on a specific key.
3. The system loads the `ApiSecret` by ID, confirms the current user owns it, and destroys the record.
4. A flash notice confirms the revocation; no error message appears.
5. The user is redirected back to the settings page.

### Revocation fails

1. An authenticated user triggers revocation, but the underlying `destroy` call fails (e.g., due to a database error).
2. The `ApiSecret` record remains in the database.
3. A flash error message is shown instructing the user to contact support; no notice appears.
4. The user is redirected back to the settings page.

## Failures / Exceptions

- Attempting to revoke a non-existent API key raises `ActiveRecord::RecordNotFound`.
- Attempting to revoke another user's API key raises `Pundit::NotAuthorizedError`.
- Suspended or spam-flagged users are denied permission to create new API keys by the `ApiSecretPolicy`.
- Unauthenticated users are denied all actions and receive a `Pundit::NotAuthorizedError`.
