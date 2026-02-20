---
id: "01KHY7PZQJNFAJNZJ973W5TW96"
name: "ai_comment_helpfulness_assessor_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/comment_helpfulness_assessor.rb
- app/sanitizers/comment_email_scrubber.rb
- app/services/ai/comment_check.rb
- app/workers/comments/send_email_notification_worker.rb
- spec/services/ai/comment_helpfulness_assessor_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::CommentHelpfulnessAssessor` within the comments domain.

### Behavioral Areas

- **helpful?**: Ensures correct behavior under the specified conditions
- **when AI returns YES**: returns true
- **when AI returns NO**: returns true
- **when AI returns yes (lowercase)**: returns true
- **when AI returns a response containing YES**: returns true
- **when AI raises an error**: returns false and logs error
- **with top-level comment**: builds prompt with top-level context
- **with reply comment**: builds prompt with top-level context

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/comment_helpfulness_assessor.rb` -- business logic orchestration and domain operations
- `app/sanitizers/comment_email_scrubber.rb`
- **Service layer**: `app/services/ai/comment_check.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/comments/send_email_notification_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

### S-2: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-3: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

### S-4: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

### S-5: returns false and logs error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false and logs error

### S-6: builds prompt with top-level context

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** builds prompt with top-level context

### S-7: builds prompt with parent comment context

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** builds prompt with parent comment context

