---
id: "01KHY9702BD6SEKKY87HEX92D6"
name: "github_repos_sync_worker_updates_repo_data"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/github_repos/repo_sync_worker.rb
- spec/workers/github_repos/repo_sync_worker_spec.rb (Test)

## Functional Overview

`GithubRepos::RepoSyncWorker` is a Sidekiq job that synchronizes a single `GithubRepo` record with the latest data from the GitHub API. It runs on the `low_priority` queue with up to 10 retries and `until_executing` uniqueness. It fetches the repository by its `full_name`, updates all metadata fields, and handles various error conditions by either destroying stale records or allowing Sidekiq to retry.

## Scenarios

### Successful sync updates repository metadata

1. The worker looks up the `GithubRepo` by ID. If the record no longer exists, it exits silently.
2. If the owning user has no GitHub identity, the worker exits silently.
3. The worker fetches the repository from the GitHub API using the repo's `full_name`.
4. All metadata fields are updated: `github_id_code`, `name`, `description`, `language`, `fork`, `bytes_size`, `watchers_count`, `stargazers_count`, and `info_hash`.
5. The `updated_at` timestamp is always touched, even if no data changed, to prevent re-enqueueing by the batch scheduler.

### User timestamp is touched with cooldown

1. After a successful sync, if the user's `github_repos_updated_at` is older than 30 minutes, the system touches it.
2. If it was updated within the last 30 minutes, the touch is skipped to avoid excessive writes during batch syncs.

### Permanently inaccessible repos are destroyed

1. If the GitHub API returns `NotFound`, the local `GithubRepo` record is destroyed.
2. If the API returns `Unauthorized`, the record is destroyed.
3. If the API returns `AccountSuspended`, the record is destroyed.
4. If the API returns `RepositoryUnavailable`, the record is destroyed.
5. If a `ClientError` with "Repository access blocked" message is received, the record is destroyed.

### Transient errors are retried

1. If the GitHub API returns a `ServerError` or an unexpected `ClientError`, the exception is re-raised, allowing Sidekiq's retry mechanism to handle it.
2. The repository record is preserved during transient failures.

## Key Members

- `TOUCH_USER_COOLDOWN` — 30-minute cooldown between user timestamp touches
