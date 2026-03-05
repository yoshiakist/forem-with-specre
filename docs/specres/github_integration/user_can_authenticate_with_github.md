---
id: "01KJ1SC4G6BA2RNA55TP5WGNVN"
name: "user_can_authenticate_with_github"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/authentication/providers/github.rb`
- `spec/services/authentication/providers/github_spec.rb` (Test)
- `spec/system/authentication/user_logs_in_with_github_spec.rb` (Test)

## Functional Overview

The `Authentication::Providers::Github` class implements the GitHub OAuth provider within Forem's authentication framework. It extends the abstract `Provider` base class and uses omniauth-github as its backend. The class is responsible for supplying the GitHub-specific sign-in path (routed through `Authentication::Paths`), extracting the correct user attributes from an OAuth payload for both new and returning users, and safely fetching the remote profile image URL via `Images::SafeRemoteProfileImageUrl`. For new users, it maps GitHub's email, nickname, display name, and avatar; for existing users, it keeps the stored GitHub username in sync with the current OAuth payload.

## Design Intent

The provider passes the `auth_payload` through a no-op `cleanup_payload` override. This satisfies the base class contract (which raises `SubclassResponsibility` by default) while deliberately retaining the full GitHub payload, implying GitHub credentials require no scrubbing before use — unlike providers that might strip tokens or sensitive fields.

## Key Members

- `OFFICIAL_NAME` — human-readable display name `"GitHub"`, used in UI labels.
- `SETTINGS_URL` — direct link to the user's GitHub application settings (`https://github.com/settings/applications`), surfaced in the platform's connected-accounts UI.
- `new_user_data` — hash returned during first-time OAuth sign-up; includes `email`, `github_username`, `name` (preferring `raw_info.name` over `info.name`), and a safely fetched `remote_profile_image_url`.
- `existing_user_data` — hash returned on subsequent logins; contains only `github_username` to keep it current.

## Scenarios

### New user signs up with valid GitHub credentials

1. A visitor navigates to the sign-up page and clicks "Continue with GitHub".
2. GitHub's OAuth flow completes and returns a valid payload to the callback URL.
3. The system creates a new user account, seeding it with the email, GitHub username, display name, and profile image from the payload.
4. The user is redirected to `/onboarding` and a remember token is set on the new account.

### New user signs up when their GitHub username is already taken

1. A visitor completes GitHub OAuth, but their GitHub nickname already exists as a Forem username.
2. The system still creates a new account, assigning a temporary username derived from the conflicting username.
3. The user is redirected to `/onboarding` to complete profile setup.

### Existing user logs in with valid GitHub credentials

1. A returning user with a linked GitHub identity clicks "Continue with GitHub" on the sign-up or sign-in page.
2. The system matches the OAuth payload to the existing account via email.
3. The user is logged in and redirected to `/?signin=true`.
4. The `existing_user_data` method updates the stored `github_username` to reflect the current OAuth payload.

### User initiates GitHub OAuth while already signed in

1. A signed-in user visits the GitHub OAuth authorize path directly.
2. The system recognises the active session and redirects immediately to `/?signin=true` without creating a duplicate identity.

### Authentication fails due to invalid or refused credentials

1. A visitor clicks "Continue with GitHub" but the OAuth callback returns an error (e.g., access denied, `OAuth::Unauthorized`, or a nil error object).
2. No user account is created.
3. The user is redirected to `/users/sign_in` and the sign-in button remains visible.
4. The failure event is reported to Datadog via `ForemStatsClient.increment("omniauth.failure", ...)`.

### New user account fails validation

1. GitHub returns a payload whose data violates a model constraint (e.g., display name exceeding 100 characters).
2. The system attempts to build a new user but the `User` record fails validation.
3. No account is created; the user is redirected to `/users/sign_up`.
4. The error is reported to Honeybadger.

### Sign-in path construction

1. Callers request the GitHub sign-in URL via `Authentication::Providers::Github.sign_in_path`.
2. The method delegates to `Authentication::Paths.sign_in_path` with the provider name and any additional keyword arguments (e.g., `state`).
3. The returned path always includes the canonical callback URL; a caller-supplied `callback_url` parameter is ignored to prevent open-redirect abuse.

### Community in invite-only mode hides GitHub option

1. The platform is configured in invitation-only mode.
2. A visitor navigates to the sign-up page.
3. The "Continue with GitHub" button is not rendered; an "invite only" notice is displayed instead.

## Failures / Exceptions

- **Invalid OAuth credentials**: OmniAuth failure handler intercepts the callback, prevents user creation, and redirects to `/users/sign_in`. Errors are incremented in Datadog.
- **Model validation failure**: If the data extracted from the GitHub payload produces an invalid `User` (e.g., name too long), the record is not persisted, the user is sent back to `/users/sign_up`, and the exception is forwarded to Honeybadger.
- **Username conflict**: When the GitHub nickname matches an existing Forem username, the system resolves the collision by generating a temporary username rather than rejecting the registration.
