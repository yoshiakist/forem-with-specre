---
id: "01KHY94DZ9B1PRJBC818Q9SKXB"
name: "github_repos_controller_manages_user_repos"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/github_repos_controller.rb
- app/policies/github_repo_policy.rb
- app/views/users/_integrations_github_repositories.html.erb
- spec/requests/github_repos_spec.rb (Test)
- spec/policies/github_repo_policy_spec.rb (Test)

## Functional Overview

`GithubReposController` provides HTTP endpoints for users to list their GitHub repositories and toggle which ones are featured on their Forem profile. It fetches live data from the GitHub API via `Github::OauthClient`, merges it with locally stored featured status, and cleans up repos that are no longer publicly accessible. `GithubRepoPolicy` enforces that only GitHub-authenticated, non-suspended users can access these endpoints.

## Scenarios

### Authorization requires GitHub identity and active account

1. Unauthenticated requests receive a 401 Unauthorized response.
2. Users who have not authenticated through GitHub are denied access (Pundit raises `NotAuthorizedError`).
3. Suspended or spam-flagged users are denied access.
4. The policy permits `github_id_code` and `featured` as the only modifiable attributes.

### Index lists repositories from GitHub API with featured status

1. The system fetches all public repositories for the current user from the GitHub API.
2. Repositories that match locally stored featured `GithubRepo` records are marked as `featured: true`.
3. The combined list is sorted alphabetically by name and returned as JSON.
4. If the GitHub API returns an authorization error, the system responds with 401 and an error message.

### Index cleans up stale featured repositories

1. If a locally featured repository is no longer present in the GitHub API response (deleted or made private), the local `GithubRepo` record is destroyed.
2. This prevents users from having phantom featured repos they cannot unfeature.

### update_or_create features or unfeatures a repository

1. The system fetches the repository by `github_id_code` from the GitHub API to verify it exists.
2. If the repository is not found on GitHub, the system responds with 404.
3. If found, the system upserts a `GithubRepo` record with the latest metadata and the requested `featured` status.
4. The user's `github_repos_updated_at` timestamp is touched.
5. On success, the system responds with JSON containing the `featured` status.
6. On validation failure, the system responds with 422 and error messages.

## Design Intent

The controller acts as a thin orchestration layer between the GitHub API and local persistence. By always fetching live data from GitHub on index, the UI reflects the user's current public repositories. The cleanup of stale featured repos is a compensating action that handles the case where a user deletes or privatizes a repository outside of Forem.
