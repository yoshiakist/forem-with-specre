---
id: "01KHY7Q0RVZKEP5FVP0XEPB9YS"
name: "credits_manage_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/credits/manage.rb
- app/controllers/credits_controller.rb
- app/services/credits/buy.rb
- app/services/credits/ledger.rb
- app/workers/credits/sync_counter_cache.rb
- spec/services/credits/manage_spec.rb

## Functional Overview

This specification defines the expected behavior of `Credits::Manage` within the credits domain.

### Behavioral Areas

- **When the the service is called**: Ensures correct behavior under the specified conditions
- **when user add an amount of credits**: adds user credits
- **when user removes the proper amount of credits**: adds user credits
- **when remove the proper amount of credits for organizations**: adds user credits
- **when adds an amount of credits for organizations**: adds user credits

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/credits/manage.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/credits_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/credits/buy.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/credits/ledger.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/credits/sync_counter_cache.rb` -- asynchronous job processing


## Scenarios

### S-1: adds user credits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds user credits

### S-2: removes user credits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes user credits

### S-3: removes org credits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes org credits

### S-4: adds org credits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds org credits

