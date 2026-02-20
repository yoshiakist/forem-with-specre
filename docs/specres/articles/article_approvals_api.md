---
id: "01KHY7PZETESPNKWHYWJ82RN8P"
name: "article_approvals_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/article_approvals_controller.rb
- spec/requests/article_approvals_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ArticleApprovals"` within the articles domain.

### Behavioral Areas

- **ArticleApprovals**: Ensures correct behavior under the specified conditions
- **POST article_approvals**: Ensures correct behavior under the specified conditions
- **when user is not tag mod**: does allow update when any tag requires approval
- **when user is a tag mod**: does allow update when any tag requires approval
- **when user is admin**: does allow update when any tag requires approval

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/article_approvals_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: does not allow update

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow update

### S-2: does allow update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does allow update

### S-3: does allow update when any tag requires approval

- **Given** the system is in a standard operational state
- **When** any tag requires approval
- **Then** does allow update

### S-4: does not allow update when multiple tags and none require approval

- **Given** the system is in a standard operational state
- **When** multiple tags and none require approval
- **Then** does not allow update

### S-5: does not allow update with one tag and does not require approval

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow update with one tag and does not require approval

### S-6: does allow update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does allow update

