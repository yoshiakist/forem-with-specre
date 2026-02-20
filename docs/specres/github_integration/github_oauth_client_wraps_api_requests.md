---
id: "01KHY930CEJV5QRQEBKVS095AX"
name: "github_oauth_client_wraps_api_requests"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/github/oauth_client.rb
- app/services/github/errors.rb
- spec/services/github/oauth_client_spec.rb (Test)

## Functional Overview

`Github::OauthClient` is a wrapper around the Octokit.rb gem that provides credential management, error translation, and observability for all GitHub API interactions. It accepts either a `client_id`/`client_secret` pair (app-level auth) or an `access_token` (user-level auth). All Octokit methods are proxied via `method_missing` with automatic error handling that translates Octokit exceptions into the `Github::Errors` hierarchy.

## Scenarios

### Credential validation on initialization

1. If an `access_token` is provided and non-empty, the client initializes successfully with token-based auth.
2. If both `client_id` and `client_secret` are provided and non-empty, the client initializes with app-level auth.
3. If credentials are missing, empty, or incomplete, the system raises `ArgumentError`.
4. When no credentials are passed, the system falls back to `Settings::Authentication.github_key` and `github_secret`.

### User-scoped client creation

1. `for_user` extracts the GitHub OAuth token from the user's GitHub identity record.
2. It returns a new `OauthClient` initialized with that access token.

### Method delegation to Octokit with error wrapping

1. Any method call not defined on `OauthClient` is delegated to the underlying `Octokit::Client`.
2. On first invocation, the method is dynamically defined on the class for efficient subsequent calls.
3. Each delegated call is wrapped in Honeycomb instrumentation.
4. If Octokit raises an error, it is recorded to Honeycomb and StatsD, then translated to the corresponding `Github::Errors` class.

### Error translation maps Octokit exceptions to domain errors

1. If the Octokit exception class name matches a known `Github::Errors` subclass (e.g., `NotFound`, `Unauthorized`, `AccountSuspended`, `RepositoryUnavailable`), that specific error is raised.
2. If the exception is an unrecognized `Octokit::ClientError`, `Github::Errors::ClientError` is raised.
3. If the exception is an unrecognized `Octokit::ServerError`, `Github::Errors::ServerError` is raised.
4. All other Octokit errors are raised as `Github::Errors::Error`.

### Faraday middleware configures retries and timeouts

1. The Faraday stack includes automatic retry on `Octokit::ServerError`.
2. Connection timeouts are set to 5 seconds for open and write, 30 seconds for read.

## Key Members

- `Github::Errors::NotFound` — GitHub resource does not exist (404)
- `Github::Errors::Unauthorized` — invalid or expired credentials (401)
- `Github::Errors::AccountSuspended` — target GitHub account is suspended (403)
- `Github::Errors::RepositoryUnavailable` — repository access is blocked (403)
- `Github::Errors::ClientError` — catch-all for 4xx errors
- `Github::Errors::ServerError` — catch-all for 5xx errors
- `Github::Errors::InvalidRepository` — invalid repository identifier (inherits `ArgumentError`)
