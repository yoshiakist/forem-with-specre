---
id: "01KHY7Q1ASJRHQWP8Z2ZF7Z462"
name: "github_repos_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/github_repos_controller.rb
- spec/requests/github_repos_spec.rb

## Functional Overview

This specification defines the expected behavior of `"GithubRepos"` within the github_integration domain.

### Behavioral Areas

- **GithubRepos**: Ensures correct behavior under the specified conditions
- **GET /github_repos**: Ensures correct behavior under the specified conditions
- **when user is unauthorized**: returns unauthorized if the user is not signed in
- **when user is authorized**: returns unauthorized if the user is not signed in
- **POST /github_repos/update_or_create**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/github_repos_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns unauthorized if the user is not signed in

- **Given** the user is not signed in
- **When** the action is triggered
- **Then** returns unauthorized

### S-2: returns unauthorized if the user not has authenticated through GitHub

- **Given** the user not has authenticated through GitHub
- **When** the action is triggered
- **Then** returns unauthorized

### S-3: returns unauthorized if the user is not authorized to perform the GitHub API cal...

- **Given** the user is not authorized to perform the GitHub API call
- **When** the action is triggered
- **Then** returns unauthorized

### S-4: returns 200 on success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 200 on success

### S-5: returns repositories with the correct JSON representation

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns repositories with the correct JSON representation

### S-6: deletes repositories which are no longer publicly accessible

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes repositories which are no longer publicly accessible

### S-7: returns 200 and json response on success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 200 and json response on success

### S-8: returns 404 if no repository is found

- **Given** no repository is found
- **When** the action is triggered
- **Then** returns 404

### S-9: updates the current user github_repos_updated_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the current user github_repos_updated_at

### S-10: allows the repo to be featured

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the repo to be featured

### S-11: allows the repo to be unfeatured

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the repo to be unfeatured

