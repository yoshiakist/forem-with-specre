---
id: "01KHY7Q1BTQCX7W0V1GJY6B3EY"
name: "subforem_reassignment_service_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/subforem_reassignment_service.rb
- app/services/ai/subforem_finder.rb
- app/services/images/generate_subforem_images.rb
- app/services/notifications/subforem_change_notification/send.rb
- app/services/subforem_moderators/add.rb
- app/services/subforem_moderators/add_trusted_role.rb
- app/services/subforem_moderators/remove.rb
- spec/services/subforem_reassignment_service_spec.rb

## Functional Overview

This specification defines the expected behavior of `SubforemReassignmentService` within the subforems domain.

### Behavioral Areas

- **check_and_reassign**: Ensures correct behavior under the specified conditions
- **when article has an offtopic automod label**: reassigns the article to the new subforem
- **when AI finds an appropriate subforem**: reassigns the article to the new subforem
- **when AI does not find an appropriate subforem**: reassigns the article to the new subforem
- **when AI finds a misc subforem as fallback**: reassigns the article to the new subforem
- **when AI finds a non-discoverable subforem**: reassigns the article to the new subforem
- **when AI service raises an error**: logs the error
- **when user has disabled subforem reassignment**: reassigns the article to the new subforem

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/subforem_reassignment_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/subforem_finder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/images/generate_subforem_images.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/subforem_change_notification/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_moderators/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_moderators/remove.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: reassigns the article to the new subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** reassigns the article to the new subforem

### S-2: sends a notification about the change

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends a notification about the change

### S-3: logs the reassignment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the reassignment

### S-4: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

### S-5: updates the automod label to on-topic equivalent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the automod label to on-topic equivalent

### S-6: does not reassign the article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not reassign the article

### S-7: does not send a notification

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send a notification

### S-8: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-9: reassigns the article to the misc subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** reassigns the article to the misc subforem

### S-10: sends a notification about the change to misc subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends a notification about the change to misc subforem

### S-11: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

### S-12: updates the automod label to on-topic equivalent for misc subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the automod label to on-topic equivalent for misc subforem

