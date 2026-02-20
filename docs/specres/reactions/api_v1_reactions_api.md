---
id: "01KHY7Q0FQQD2KFHRTVJTKPZ0D"
name: "api_v1_reactions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/privileged_reactions_controller.rb
- app/controllers/admin/reactions_controller.rb
- app/controllers/api/v1/reactions_controller.rb
- app/controllers/reactions_controller.rb
- app/services/users/confirm_flag_reactions.rb
- app/workers/users/confirm_flag_reactions_worker.rb
- spec/requests/api/v1/reactions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::Reactions"` within the reactions domain.

### Behavioral Areas

- **Api::V1::Reactions**: Ensures correct behavior under the specified conditions
- **when user is authorized**: returns unauthorized
- **when unauthenticated and post to toggle**: invalidates reaction_counts_for_reactable cache when creating a reaction
- **when unauthorized and post to toggle**: returns unauthorized
- **when authorized and post to toggle**: returns unauthorized
- **when user is authorized**: returns unauthorized
- **when toggled successfully**: invalidates reaction_counts_for_reactable cache when creating a reaction
- **when toggled unsuccessfully**: invalidates reaction_counts_for_reactable cache when creating a reaction

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/privileged_reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/reactions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/users/confirm_flag_reactions.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/users/confirm_flag_reactions_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-2: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-3: responds with success

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with success

### S-4: responds with expected JSON

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with expected JSON

### S-5: responds with success

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with success

### S-6: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-7: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-8: responds with success

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with success

### S-9: responds with expected JSON

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with expected JSON

### S-10: responds with success

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with success

### S-11: invalidates reaction_counts_for_reactable cache when creating a reaction

- **Given** the system is in a standard operational state
- **When** creating a reaction
- **Then** invalidates reaction_counts_for_reactable cache

### S-12: invalidates reaction_counts_for_reactable cache when toggling a reaction

- **Given** the system is in a standard operational state
- **When** toggling a reaction
- **Then** invalidates reaction_counts_for_reactable cache

