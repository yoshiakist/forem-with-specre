---
id: "01KHY7Q0GY8Y5VSPCSKQA26R2Y"
name: "reactions_update_relevant_scores_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/reactions/update_relevant_scores_worker.rb
- app/controllers/admin/privileged_reactions_controller.rb
- app/controllers/admin/reactions_controller.rb
- app/controllers/api/v1/reactions_controller.rb
- app/controllers/reactions_controller.rb
- app/services/notifications/reactions/reaction_data.rb
- app/services/notifications/reactions/send.rb
- app/services/users/confirm_flag_reactions.rb
- app/workers/reactions/bust_homepage_cache_worker.rb
- app/workers/reactions/bust_reactable_cache_worker.rb
- app/workers/users/confirm_flag_reactions_worker.rb
- spec/workers/reactions/update_relevant_scores_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Reactions::UpdateRelevantScoresWorker` within the reactions domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/reactions/update_relevant_scores_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/privileged_reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/reactions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/notifications/reactions/reaction_data.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/reactions/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/confirm_flag_reactions.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/reactions/bust_homepage_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/reactions/bust_reactable_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/confirm_flag_reactions_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: kicks off point update if article

- **Given** article
- **When** the action is triggered
- **Then** kicks off point update

### S-2: does not kick off points updater if not comment reaction

- **Given** not comment reaction
- **When** the action is triggered
- **Then** does not kick off points updater

### S-3: does not kick off points updater if reaction is non-public

- **Given** reaction is non-public
- **When** the action is triggered
- **Then** does not kick off points updater

### S-4: updates the reactable Article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the reactable Article

### S-5: recalculates score if reactable is User

- **Given** reactable is User
- **When** the action is triggered
- **Then** recalculates score

### S-6: updates the reactable Comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the reactable Comment

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-8: uses a throttled call for syncing the reactions count

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses a throttled call for syncing the reactions count

