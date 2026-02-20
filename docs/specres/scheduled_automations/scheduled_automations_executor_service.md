---
id: "01KHY7Q1JG53C9Q9F0SMJST6BE"
name: "scheduled_automations_executor_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/scheduled_automations/executor.rb
- app/controllers/admin/scheduled_automations_controller.rb
- app/helpers/scheduled_automations_helper.rb
- app/services/scheduled_automations/article_content_badge_awarder.rb
- app/services/scheduled_automations/first_post_badge_awarder.rb
- app/services/scheduled_automations/warm_welcome_badge_awarder.rb
- app/workers/scheduled_automations/process_worker.rb
- spec/services/scheduled_automations/executor_spec.rb

## Functional Overview

This specification defines the expected behavior of `ScheduledAutomations::Executor` within the scheduled_automations domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **call**: calls the AI service
- **when automation is already running**: executes the automation
- **when automation executes successfully**: executes the automation
- **when action is publish_article**: creates a draft article when action is create_draft
- **when service returns nil**: returns a failure result
- **with additional instructions**: returns success with no article
- **with string values in action_config**: applies tags from action_config

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/scheduled_automations/executor.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/scheduled_automations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/scheduled_automations_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/scheduled_automations/article_content_badge_awarder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/first_post_badge_awarder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/warm_welcome_badge_awarder.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/scheduled_automations/process_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: executes the automation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** executes the automation

### S-2: returns a failure result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a failure result

### S-3: marks automation as running

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks automation as running

### S-4: calls the AI service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the AI service

### S-5: creates an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an article

### S-6: creates a draft article when action is create_draft

- **Given** the system is in a standard operational state
- **When** action is create_draft
- **Then** creates a draft article

### S-7: applies tags from action_config

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** applies tags from action_config

### S-8: sets the next run time

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the next run time

### S-9: updates last_run_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates last_run_at

### S-10: returns success result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success result

### S-11: creates a published article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a published article

### S-12: returns success with no article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success with no article

