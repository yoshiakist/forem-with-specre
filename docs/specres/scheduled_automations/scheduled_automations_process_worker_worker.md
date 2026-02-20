---
id: "01KHY7Q1JKM8RP75X1TERDA871"
name: "scheduled_automations_process_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/scheduled_automations/process_worker.rb
- app/controllers/admin/scheduled_automations_controller.rb
- app/helpers/scheduled_automations_helper.rb
- app/services/scheduled_automations/article_content_badge_awarder.rb
- app/services/scheduled_automations/executor.rb
- app/services/scheduled_automations/first_post_badge_awarder.rb
- app/services/scheduled_automations/warm_welcome_badge_awarder.rb
- spec/workers/scheduled_automations/process_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `ScheduledAutomations::ProcessWorker` within the scheduled_automations domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when warm welcome badge exists**: Ensures correct behavior under the specified conditions
- **when automation does not exist**: creates the automation automatically
- **when no community bot exists**: Ensures correct behavior under the specified conditions
- **when automation already exists**: creates the automation automatically
- **when warm welcome badge does not exist**: does not create automation and logs warning
- **when executing due automations**: executes automations that are due

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/scheduled_automations/process_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/scheduled_automations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/scheduled_automations_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/scheduled_automations/article_content_badge_awarder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/executor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/first_post_badge_awarder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/warm_welcome_badge_awarder.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: creates the automation automatically

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates the automation automatically

### S-2: schedules next run for Friday at 9 AM

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** schedules next run for Friday at 9 AM

### S-3: does not create automation and logs warning

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create automation and logs warning

### S-4: does not create a duplicate automation

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a duplicate automation

### S-5: does not create automation

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create automation

### S-6: executes automations that are due

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** executes automations that are due

