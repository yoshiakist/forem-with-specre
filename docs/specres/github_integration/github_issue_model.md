---
id: "01KHY7Q1AJA2PWZEMVK9SX1Z45"
name: "github_issue_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/github_tag/github_issue_tag.rb
- app/models/github_issue.rb
- app/models/github_repo.rb
- spec/models/github_issue_spec.rb

## Functional Overview

This specification defines the expected behavior of `GithubIssue` within the github_integration domain.

### Behavioral Areas

- **.find_or_fetch**: Ensures correct behavior under the specified conditions
- **when retrieving an issue**: saves a new issue
- **when retrieving a pull request**: Ensures correct behavior under the specified conditions
- **when retrieving a comment**: saves a new issue comment

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/github_tag/github_issue_tag.rb` -- custom Markdown/Liquid embed rendering
- **Model layer**: `app/models/github_issue.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/github_repo.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate length of url.is at most 400
- validate inclusion of category.in array %w[issue issue comment]
- validate presence of url

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: saves a new issue

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** saves a new issue

### S-3: retrieves an existing issue

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retrieves an existing issue

### S-4: saves the proper fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** saves the proper fields

### S-5: saves a new issue

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** saves a new issue

### S-6: retrieves an existing issue

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retrieves an existing issue

### S-7: saves the proper fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** saves the proper fields

### S-8: saves a new issue comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** saves a new issue comment

### S-9: retrieves an existing issue comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retrieves an existing issue comment

### S-10: saves the proper fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** saves the proper fields

### S-11: saves HTML in .processed_html

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** saves HTML in .processed_html

### S-12: raises Github::Errors::NotFound if the issue is not found

- **Given** the issue is not found
- **When** the action is triggered
- **Then** raises Github::Errors::NotFound

