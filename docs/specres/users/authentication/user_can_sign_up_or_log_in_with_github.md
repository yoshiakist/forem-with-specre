---
id: "01KJBK9T82MG157560A1HGHHXJ"
name: "user_can_sign_up_or_log_in_with_github"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/omniauth_callbacks_controller.rb`
- `app/services/authentication/authenticator.rb`
- `app/services/authentication/providers.rb`
- `app/services/authentication/providers/provider.rb`
- `app/services/authentication/providers/github.rb`
- `app/services/authentication/paths.rb`
- `app/models/identity.rb`
- `app/errors/authentication/errors.rb`
- `app/helpers/authentication_helper.rb`
- `app/views/shared/_authentication_actions.html.erb` (Template)
- `app/views/shared/_authentication_title.html.erb` (Template)
- `app/views/shared/_authentication_description.html.erb` (Template)
- `app/views/devise/shared/_authorization_error.html.erb` (Template)
- `app/views/users/_github_repositories_area.html.erb` (Template)
- `app/views/users/_integrations_github_repositories.html.erb` (Template)
- `spec/system/authentication/user_logs_in_with_github_spec.rb` (Test)
- `spec/services/authentication/providers/github_spec.rb` (Test)

## Functional Overview

When a visitor clicks "Continue with GitHub", the browser is redirected to GitHub's OAuth authorization endpoint via `Authentication::Providers::Github.sign_in_path`. Upon approval, GitHub redirects back to `/users/auth/github/callback`, where `OmniauthCallbacksController` receives the OmniAuth payload and delegates to `Authentication::Authenticator`. The authenticator builds or looks up an `Identity` record keyed on the provider UID, guards against spammy email domains and previously-suspended usernames, then either creates a new `User` (new signup) or updates an existing one (returning login). On success the user is signed in via Devise and redirected to onboarding (new users) or the home feed (returning users). This controller and the shared infrastructure classes (`Authenticator`, `Identity`, `Paths`, `Errors`) form the OmniAuth backbone referenced by all other OAuth provider cards.

## Design Intent

CSRF protection is selectively bypassed for the GitHub callback path when the request's origin is `https://github.com`, because Rails cannot whitelist arbitrary trusted third-party origins in its standard CSRF mechanism. All other requests remain protected. The authenticator is intentionally provider-agnostic: it delegates all GitHub-specific field mapping to `Authentication::Providers::Github`, keeping the core sign-in/sign-up logic reusable across providers.

## Scenarios

### New user signs up with GitHub

1. Visitor navigates to the sign-up page and clicks "Continue with GitHub".
2. Browser is redirected to GitHub with the callback URL embedded as a parameter.
3. User authorizes the Forem application on GitHub.
4. GitHub redirects to `/users/auth/github/callback` with an OAuth payload.
5. The system builds an `Identity` from the payload, verifies the email domain is not spammy, and confirms the username is not previously suspended.
6. A new `User` is created with the GitHub email, nickname, name, and profile image; the identity is linked and saved in a transaction.
7. User is signed in, a remember-me cookie is set, and the browser is redirected to `/onboarding`.

### Returning user logs in with GitHub

1. Registered user navigates to the sign-up/sign-in page and clicks "Continue with GitHub".
2. GitHub redirects back with the same OAuth payload as before.
3. The existing `Identity` (matched by provider + UID) is found, and the associated `User` is loaded.
4. The user's `github_username` is updated; email is only updated if the account is unconfirmed.
5. User is signed in and redirected to `/?signin=true`.

### Already-logged-in user revisits the GitHub OAuth path

1. A signed-in user navigates to the GitHub authorize path (e.g., to connect the identity).
2. The authenticator detects that the current user already has a GitHub identity and returns immediately without creating duplicates.
3. User is redirected to the home feed.

### GitHub returns invalid or denied credentials

1. GitHub returns an error or the user denies authorization.
2. OmniAuth triggers the shared `failure` action.
3. The failure is recorded in Datadog (`omniauth.failure`) with provider, error class, and reason tags.
4. Honeybadger is notified if an error object is present.
5. User is redirected to `/users/sign_in` with no new account created.

### Invite-only community blocks GitHub signup

1. The community is configured in invite-only mode.
2. The sign-up page does not render the "Continue with GitHub" button.
3. Users see a message indicating the community is invite-only and cannot initiate the OAuth flow.

## Failures / Exceptions

- `Authentication::Errors::PreviouslySuspended` — raised when the GitHub username matches a previously-suspended username; user sees a global notice and is redirected to root.
- `Authentication::Errors::SpammyEmailDomain` — raised when the email domain from the GitHub payload is on the block-list; handled the same way as `PreviouslySuspended`.
- Validation failure (e.g., name too long) — the user is not persisted; errors are flashed, Honeybadger is notified, and the browser is redirected to `/users/sign_up`.
- Unhandled `StandardError` — caught at the controller level; Honeybadger is notified and the user is redirected to `/users/sign_up` with a generic error message.
