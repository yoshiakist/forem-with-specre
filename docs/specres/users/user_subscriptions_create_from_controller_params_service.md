---
id: "01KHY7PZZA89PZ5P5A1FKB4XZ0"
name: "user_subscriptions_create_from_controller_params_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/user_subscriptions/create_from_controller_params.rb
- app/controllers/user_subscriptions_controller.rb
- app/services/user_subscriptions/is_subscribed_cache_checker.rb
- spec/services/user_subscriptions/create_from_controller_params_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserSubscriptions::CreateFromControllerParams` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/user_subscriptions/create_from_controller_params.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/user_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/user_subscriptions/is_subscribed_cache_checker.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns an error for an invalid source type

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for an invalid source type

### S-2: returns an error for an invalid source

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for an invalid source

### S-3: returns an error for an email mismatch

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for an email mismatch

### S-4: returns an error if a UserSubscription can

- **Given** a UserSubscription can
- **When** the action is triggered
- **Then** returns an error

### S-5: creates a UserSubscription

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a UserSubscription

