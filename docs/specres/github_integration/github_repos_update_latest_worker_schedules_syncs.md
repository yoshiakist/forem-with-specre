---
id: "01KHY987S3SNX2YV4C0ZHSHEK3"
name: "github_repos_update_latest_worker_schedules_syncs"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/github_repos/update_latest_worker.rb
- spec/workers/github_repos/update_latest_worker_spec.rb (Test)

## Functional Overview

`GithubRepos::UpdateLatestWorker` is a Sidekiq job that acts as a batch scheduler for repository synchronization. It runs on the `medium_priority` queue and delegates to `GithubRepo.update_to_latest`, which enqueues individual `RepoSyncWorker` jobs for all repositories that have not been updated in 26+ hours.

## Scenarios

### Worker delegates to GithubRepo.update_to_latest

1. When performed, the worker calls `GithubRepo.update_to_latest`.
2. This triggers bulk enqueueing of `GithubRepos::RepoSyncWorker` for each stale repository.
3. The worker runs on the `medium_priority` queue with up to 10 retries.

## Design Intent

This worker separates the scheduling concern (which repos need syncing) from the execution concern (how to sync a single repo). It is designed to be invoked periodically by a cron-like scheduler, keeping repository metadata fresh without placing all sync work in a single long-running job.
