---
id: "01KHY7Q1AMT0S39RXY1FQ8AVKR"
name: "github_repo_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/github_repos_controller.rb
- app/models/github_repo.rb
- app/policies/github_repo_policy.rb
- app/services/ai/github_repo_recap.rb
- app/models/github_issue.rb
- spec/models/github_repo_spec.rb

## Functional Overview

This specification defines the expected behavior of `GithubRepo` within the github_integration domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **when callbacks are triggered after save**: Ensures correct behavior under the specified conditions
- **clearing caches**: busts the correct caches
- **.upsert**: Ensures correct behavior under the specified conditions
- **::update_to_latest**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/github_repos_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/github_repo.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/github_repo_policy.rb` -- authorization and access control rules
- **Service layer**: `app/services/ai/github_repo_recap.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/github_issue.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of name
- validate presence of url
- validate uniqueness of github id code
- validate uniqueness of url
- validate url of url

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-3: busts the correct caches

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the correct caches

### S-4: creates a new repo

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new repo

### S-5: creates a repo for the given user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a repo for the given user

### S-6: returns an existing repo updated with new params

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an existing repo updated with new params

### S-7: enqueues GithubRepos::RepoSyncWorker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues GithubRepos::RepoSyncWorker

