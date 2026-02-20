---
id: "01KHY7Q17EWWP62DP57A82M1Y5"
name: "github_tag_github_readme_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/github_tag/github_readme_tag.rb
- app/liquid_tags/github_tag.rb
- app/liquid_tags/github_tag/github_issue_tag.rb
- spec/liquid_tags/github_tag/github_readme_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `GithubTag::GithubReadmeTag` within the liquid_tags domain.

### Behavioral Areas

- **id**: Ensures correct behavior under the specified conditions
- **options**: rejects invalid options
- **regressions**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/github_tag/github_readme_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/github_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/github_tag/github_issue_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: rejects GitHub URL without domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects GitHub URL without domain

### S-2: rejects invalid GitHub repository URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid GitHub repository URL

### S-3: rejects a non existing GitHub repository URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects a non existing GitHub repository URL

### S-4: renders a repository URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a repository URL

### S-5: renders a repository path

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a repository path

### S-6: renders a repository URL with a trailing slash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a repository URL with a trailing slash

### S-7: renders a repository path with a trailing slash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a repository path with a trailing slash

### S-8: renders a repository URL with a fragment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a repository URL with a fragment

### S-9: renders a repository with a missing README

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a repository with a missing README

### S-10: renders a repository with relative links in README

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a repository with relative links in README

### S-11: rejects invalid options

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid options

### S-12: accepts 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts 

