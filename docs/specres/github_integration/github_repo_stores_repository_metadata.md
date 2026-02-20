---
id: "01KHY90CYGYNH31CN6DQN705HH"
name: "github_repo_stores_repository_metadata"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/github_repo.rb
- app/views/users/_github_repositories_area.html.erb
- spec/models/github_repo_spec.rb (Test)

## Functional Overview

`GithubRepo` is an ActiveRecord model that persists GitHub repository metadata for a user. It stores repository name, URL, GitHub ID code, description, language, fork status, star/watchers counts, and an `info_hash` for additional serialized data. It supports upsert semantics for idempotent sync from the GitHub API and triggers edge-cache invalidation on the owning user's profile whenever a repo is saved or destroyed.

## Scenarios

### Validation ensures required fields and uniqueness

1. The system requires `name`, `url`, and `github_id_code` to be present.
2. The system enforces that `url` is a valid URL format.
3. The system enforces uniqueness on both `url` and `github_id_code`.

### Upsert creates or updates a repository by GitHub ID or URL

1. Given a set of repository params including `github_id_code`, `name`, and `url`:
2. If no existing `GithubRepo` matches the `github_id_code` or `url` for the user, a new record is created.
3. If an existing record matches by `github_id_code` or `url`, that record is updated with the new params.
4. The record is associated with the given user.

### Cache clearing on save and destroy

1. After a `GithubRepo` is saved or destroyed, the system touches the owning user's `updated_at` timestamp.
2. The system busts the edge cache for the user's profile path (three URL variants).
3. If the repo has no associated user, cache clearing is skipped.

### Featured scope filters pinned repositories

1. The `featured` scope returns only repositories where `featured` is true.

### Batch sync enqueues workers for stale repositories

1. `update_to_latest` selects all repos not updated in the last 26 hours.
2. It enqueues a `GithubRepos::RepoSyncWorker` job for each stale repo ID.

## Design Intent

Repositories are synced from GitHub as a read-through cache — the authoritative data lives on GitHub, and Forem stores a snapshot for display on user profiles. The upsert pattern prevents duplicate records when the same repo is synced multiple times. Cache busting ensures profile pages reflect repo changes immediately.
