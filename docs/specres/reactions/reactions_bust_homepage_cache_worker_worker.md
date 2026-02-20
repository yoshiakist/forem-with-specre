---
id: "01KHY7Q0GS61YGWVYD1DY08S6F"
name: "reactions_bust_homepage_cache_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/reactions/bust_homepage_cache_worker.rb
- app/controllers/admin/privileged_reactions_controller.rb
- app/controllers/admin/reactions_controller.rb
- app/controllers/api/v1/reactions_controller.rb
- app/controllers/reactions_controller.rb
- app/services/notifications/reactions/reaction_data.rb
- app/services/notifications/reactions/send.rb
- app/services/users/confirm_flag_reactions.rb
- app/workers/reactions/bust_reactable_cache_worker.rb
- app/workers/reactions/update_relevant_scores_worker.rb
- app/workers/users/confirm_flag_reactions_worker.rb
- spec/workers/reactions/bust_homepage_cache_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Reactions::BustHomepageCacheWorker` within the reactions domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/reactions/bust_homepage_cache_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/privileged_reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/reactions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/notifications/reactions/reaction_data.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/reactions/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/confirm_flag_reactions.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/reactions/bust_reactable_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/reactions/update_relevant_scores_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/confirm_flag_reactions_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: busts the homepage cache when reactable is an Article

- **Given** the system is in a standard operational state
- **When** reactable is an Article
- **Then** busts the homepage cache

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

