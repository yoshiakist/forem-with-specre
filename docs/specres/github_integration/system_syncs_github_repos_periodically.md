---
id: "01KJ1SBPYYJH4XJS6P8SW1HSG2"
name: "system_syncs_github_repos_periodically"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/workers/github_repos/repo_sync_worker.rb`
- `app/workers/github_repos/update_latest_worker.rb`
- `spec/workers/github_repos/repo_sync_worker_spec.rb` (Test)
- `spec/workers/github_repos/update_latest_worker_spec.rb` (Test)

## Functional Overview

The system periodically synchronizes GitHub repository data for users via two background workers. `UpdateLatestWorker` triggers a bulk refresh of all tracked GitHub repos by delegating to `GithubRepo.update_to_latest`. For individual repos, `RepoSyncWorker` fetches fresh metadata from the GitHub API using the user's OAuth credentials and updates stored fields such as name, description, language, fork status, byte size, watcher count, and star count. After a successful sync, the user's `github_repos_updated_at` timestamp is refreshed subject to a 30-minute cooldown. If the GitHub API reports the repository as not found, unauthorized, account-suspended, access-blocked, or repository-unavailable, the local record is destroyed.

## Design Intent

`RepoSyncWorker` is placed on the `low_priority` queue because individual repo syncs are non-urgent and should not compete with user-facing work. The 30-minute cooldown on touching `github_repos_updated_at` prevents excessive database writes when many repos belonging to the same user are synced in quick succession. `updated_at` on the repo record is always stamped even when none of the fetched fields change, ensuring downstream cache invalidation logic has a reliable signal (see PR #12853).

## Key Members

- `TOUCH_USER_COOLDOWN` — 30-minute threshold; the owning user's `github_repos_updated_at` is only refreshed if it was last updated more than 30 minutes ago.

## Scenarios

### Bulk update of all repos

1. `UpdateLatestWorker` is executed by the scheduler (medium-priority queue).
2. It calls `GithubRepo.update_to_latest`, which enqueues or directly updates every tracked repository record.

### Successful individual repo sync

1. `RepoSyncWorker` is invoked with a `repo_id`.
2. The system looks up the `GithubRepo` record; if it does not exist, the job exits immediately.
3. The system verifies that the repo's owner has a linked GitHub identity; if not, the job exits immediately.
4. An authenticated `Github::OauthClient` is built for the user and the current repository metadata is fetched from GitHub by full name.
5. The local record is updated with the latest name, description, language, fork status, size, watcher count, star count, full info hash, and the current timestamp.
6. If the user's `github_repos_updated_at` is older than 30 minutes, it is touched to reflect the sync.

### User with no GitHub identity

1. `RepoSyncWorker` is invoked with a `repo_id` for a user who no longer has a GitHub identity linked.
2. The system finds the repo but finds no GitHub identity on the user.
3. The job returns without making any API call or modifying any record.

## Failures / Exceptions

- If GitHub responds with `NotFound`, `Unauthorized`, `AccountSuspended`, or `RepositoryUnavailable`, the local `GithubRepo` record is destroyed.
- If GitHub responds with a `ClientError` whose message includes "Repository access blocked", the record is also destroyed.
- Any other `ClientError` (e.g., a 500 server error) is re-raised, allowing Sidekiq's retry mechanism to handle it; the repo record is preserved.
