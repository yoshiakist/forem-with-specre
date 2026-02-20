---
id: "01KHY7PZZCQA6XXE6A6CRFEVBP"
name: "user_subscriptions_is_subscribed_cache_checker_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/user_subscriptions/is_subscribed_cache_checker.rb
- app/controllers/user_subscriptions_controller.rb
- app/services/user_subscriptions/create_from_controller_params.rb
- spec/services/user_subscriptions/is_subscribed_cache_checker_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserSubscriptions::IsSubscribedCacheChecker` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/user_subscriptions/is_subscribed_cache_checker.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/user_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/user_subscriptions/create_from_controller_params.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: checks if subscribed to a thing and returns true if they are

- **Given** subscribed to a thing and returns true if they are
- **When** the action is triggered
- **Then** checks

### S-2: checks if subscribed to a thing and returns false if they are not

- **Given** subscribed to a thing and returns false if they are not
- **When** the action is triggered
- **Then** checks

