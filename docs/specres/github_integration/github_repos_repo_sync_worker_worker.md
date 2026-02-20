---
id: "01KHY7Q1AZRWBC9XHDK7G75E94"
name: "github_repos_repo_sync_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/github_repos/repo_sync_worker.rb
- app/controllers/github_repos_controller.rb
- app/workers/github_repos/update_latest_worker.rb
- spec/workers/github_repos/repo_sync_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `GithubRepos::RepoSyncWorker` within the github_integration domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/github_repos/repo_sync_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/github_repos_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/github_repos/update_latest_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: updates all repositories

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates all repositories

### S-2: updates repo updated_at even if data is unchanged

- **Given** data is unchanged
- **When** the action is triggered
- **Then** updates repo updated_at even

### S-3: does not touch repo user again if recently updated

- **Given** recently updated
- **When** the action is triggered
- **Then** does not touch repo user again

### S-4: destroys unfound repos

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys unfound repos

### S-5: destroys Unauthorized repos

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys Unauthorized repos

### S-6: destroys suspended account repos

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys suspended account repos

### S-7: destroys blocked access repos

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys blocked access repos

### S-8: retains the repo on an unexpected Github client error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retains the repo on an unexpected Github client error

