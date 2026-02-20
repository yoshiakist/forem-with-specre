---
id: "01KHY7Q17CZVJX370MWJ9ZNJQE"
name: "github_tag_github_issue_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/github_tag/github_issue_tag.rb
- app/liquid_tags/github_tag.rb
- app/liquid_tags/github_tag/github_readme_tag.rb
- spec/liquid_tags/github_tag/github_issue_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `GithubTag::GithubIssueTag` within the liquid_tags domain.

### Behavioral Areas

- **id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/github_tag/github_issue_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/github_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/github_tag/github_readme_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: rejects GitHub URL without domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects GitHub URL without domain

### S-2: rejects invalid GitHub issue URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid GitHub issue URL

### S-3: rejects a non existing GitHub issue URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects a non existing GitHub issue URL

### S-4: renders an issue URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders an issue URL

### S-5: renders an issue URL with dot character

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders an issue URL with dot character

### S-6: renders an issue URL with an issue fragment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders an issue URL with an issue fragment

### S-7: renders a pull request URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a pull request URL

### S-8: renders a pull request URL with an issue fragment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a pull request URL with an issue fragment

### S-9: renders an issue comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders an issue comment

### S-10: renders a PR comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a PR comment

