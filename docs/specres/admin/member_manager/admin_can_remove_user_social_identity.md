---
id: "01KJ9NBXAJ300R2MV2SNKRMTNJ"
name: "admin_can_remove_user_social_identity"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `spec/requests/admin/users_spec.rb` (Test)

## Functional Overview

An admin can remove a social identity (e.g., GitHub, Twitter) that is linked to a user's account. The system looks up the identity record by its ID, destroys it, and clears the corresponding `{provider}_username` field on the user. When the removed identity belongs to the GitHub provider, all of the user's stored GitHub repositories are also destroyed, because those repos are fetched via the user's GitHub OAuth token which no longer exists. On success, the admin is redirected back to the user's admin page with a success flash message. On failure, a danger flash message is shown and the admin is still redirected to the user's admin page.

## Design Intent

GitHub repositories are fetched from the API using the user's GitHub OAuth token. Without a linked GitHub identity that token is unavailable, so the repos would be stale and unrefreshable. Destroying them eagerly keeps the stored data consistent with the user's actual linked accounts. No equivalent clean-up is needed for other providers because no derived data depends on their tokens in the same way.

## Key Members

- `identity_id` — the ID of the `Identity` record to remove, submitted as a user param
- `Identity#provider` — the OAuth provider name (e.g., `"github"`, `"twitter"`) used to determine which username field to clear and whether to purge GitHub repos
- `{provider}_username` on `User` — the cached username for the given provider, set to `nil` after removal
- `GithubRepo` — associated repository records destroyed when the GitHub identity is removed

## Scenarios

### Remove a GitHub identity (also destroys GitHub repos)

1. Admin submits a DELETE request to `remove_identity` with the ID of a user's GitHub identity.
2. The system finds the `Identity` record and retrieves the associated user.
3. The identity record is destroyed.
4. The user's `github_username` field is set to `nil`.
5. All `GithubRepo` records belonging to the user are destroyed.
6. A success flash message is set and the admin is redirected to the user's admin page.

### Remove a non-GitHub identity

1. Admin submits a DELETE request to `remove_identity` with the ID of a non-GitHub identity (e.g., Twitter).
2. The system finds the `Identity` record and retrieves the associated user.
3. The identity record is destroyed.
4. The user's `{provider}_username` field (e.g., `twitter_username`) is set to `nil`.
5. GitHub repositories are left untouched.
6. A success flash message is set and the admin is redirected to the user's admin page.

## Failures / Exceptions

- If any step in the removal process raises a `StandardError`, the error message is placed in a danger flash and the admin is redirected to the user's admin page without any partial changes being surfaced to the UI.
