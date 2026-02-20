---
id: "01KHY7Q09YYEVAAWN58F5FN978"
name: "ai_badge_criteria_assessor_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/badge_criteria_assessor.rb
- app/workers/badge_achievements/send_email_notification_worker.rb
- spec/services/ai/badge_criteria_assessor_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::BadgeCriteriaAssessor` within the badges domain.

### Behavioral Areas

- **qualifies?**: Ensures correct behavior under the specified conditions
- **when AI returns YES**: returns true
- **when AI returns NO**: returns true
- **when AI returns yes (lowercase)**: returns true
- **when AI returns a response containing YES**: returns true
- **when AI raises an error**: logs the error

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/badge_criteria_assessor.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/badge_achievements/send_email_notification_worker.rb` -- asynchronous job processing


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

### S-5: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-6: logs the error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the error

