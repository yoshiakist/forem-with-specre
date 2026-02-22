---
id: "01KJ1SC2K2MHD1YYH79TBFM4VQ"
name: "user_can_feature_github_repos_on_profile"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/github_repos_controller.rb`
- `app/models/github_repo.rb`
- `app/policies/github_repo_policy.rb`
- `app/javascript/githubRepos/githubRepos.jsx`
- `app/javascript/githubRepos/singleRepo.jsx`
- `app/javascript/packs/githubRepos.jsx`
- `app/services/github/oauth_client.rb`
- `app/services/github/errors.rb`
- `app/views/users/_github_repositories_area.html.erb` (Template)
- `app/views/users/_integrations_github_repositories.html.erb` (Template)
- `spec/requests/github_repos_spec.rb` (Test)
- `spec/models/github_repo_spec.rb` (Test)
- `spec/policies/github_repo_policy_spec.rb` (Test)
- `spec/services/github/oauth_client_spec.rb` (Test)
- `app/javascript/githubRepos/__tests__/githubRepos.test.jsx` (Test)
- `app/javascript/githubRepos/__tests__/singleRepo.test.jsx` (Test)

## Functional Overview

Users who have connected their GitHub account can visit their settings page to see a list of all their public GitHub repositories, fetched live via the GitHub API using the user's OAuth access token. Each repository is displayed with its name, fork status, and current featured state. The user can toggle any repository as "featured" or not; toggling a repository calls `POST /github_repos/update_or_create`, which upserts the repository record in the database and returns the new featured state. Featured repositories are then rendered on the user's public profile page. Only users authenticated through GitHub and not suspended are authorized to access these endpoints. Repositories that were previously featured but are no longer publicly accessible on GitHub are automatically removed from the database when the list is next fetched.

## Design Intent

The controller merges live GitHub API data with locally stored featured flags on each `GET /github_repos` request rather than relying solely on stored data. This ensures the displayed repository list always reflects the user's current public repositories on GitHub, and that stale featured entries (for repos that became private or were deleted) are cleaned up automatically. The `GithubRepo.upsert` method matches by either GitHub ID or URL to handle repository renames gracefully without creating duplicates.

## Key Members

- `GithubRepo.featured` (scope) — filters repositories marked as featured for display on the user profile
- `GithubRepo.upsert(user, **params)` — finds an existing repo by `github_id_code` or `url`, updating it in place, or creates a new one
- `Github::OauthClient.for_user(user)` — instantiates an authenticated GitHub API client using the user's stored OAuth access token
- `featured` (boolean on `GithubRepo`) — the flag toggled by the user to mark a repo for display on their public profile

## Scenarios

### User views their GitHub repositories in settings

1. An authenticated user with a connected GitHub account opens the GitHub integration section of their settings page.
2. The frontend mounts the `GithubRepos` component, which immediately fetches `GET /github_repos`.
3. The controller authorizes the request via `GithubRepoPolicy#index?`, confirming the user is not suspended and has authenticated through GitHub.
4. The controller fetches all public repositories from the GitHub API using `Github::OauthClient.for_user`, cross-references the results with locally stored featured repos, and marks any matching repos as featured.
5. Any previously featured repos not returned by the GitHub API (deleted or made private) are destroyed.
6. The list is returned as JSON sorted alphabetically by repository name.
7. The frontend renders each repository as a `SingleRepo` component showing its name, fork label if applicable, and a "Select" or "Remove" button based on featured state.

### User features a repository

1. The user clicks "Select" on an unfeatured repository in the settings UI.
2. The `SingleRepo` component posts to `POST /github_repos/update_or_create` with the repository's `github_id_code` and `featured: true`.
3. The controller fetches the individual repository from the GitHub API to confirm it exists and retrieve up-to-date metadata.
4. `GithubRepo.upsert` creates or updates the local record with the new featured flag and full repository metadata.
5. The user's `github_repos_updated_at` timestamp is touched.
6. The server responds with `{ featured: true }`, and the UI updates the button to "Remove" and applies the featured row style.

### User unfeatures a repository

1. The user clicks "Remove" on a currently featured repository.
2. The same `POST /github_repos/update_or_create` flow executes with `featured: false`.
3. The server responds with `{ featured: false }`, and the UI updates the button back to "Select".

### Featured repositories appear on the user's public profile

1. When another user (or the profile owner) views the profile page, the server renders the `_github_repositories_area` partial.
2. The partial iterates over the user's featured `GithubRepo` records and displays each repo's name, description (with emoji parsing), language, and star count as a linked card.
3. The section is hidden entirely if the user has no featured repositories.

## Failures / Exceptions

- If the user is not authenticated (not signed in), `GET /github_repos` returns HTTP 401.
- If the user has not connected a GitHub account or is suspended, the policy raises `Pundit::NotAuthorizedError`, blocking access to both endpoints.
- If the GitHub API call returns an authorization error (`Github::Errors::Unauthorized`), the index action renders a JSON error with HTTP 401.
- If the specific repository requested in `update_or_create` is not found on GitHub (`Github::Errors::NotFound`), the action renders a JSON error with HTTP 404.
- If `GithubRepo` fails model validations on save, the action renders the validation errors with HTTP 422.
- If the frontend fetch fails for any reason, the `GithubRepos` component renders an accessible error alert and notifies Honeybadger.
