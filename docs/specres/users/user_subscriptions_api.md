---
id: "01KHY7PZXDJX4SJT5R43KQ564Z"
name: "user_subscriptions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/user_subscriptions_controller.rb
- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/queries/admin/gdpr_delete_requests_query.rb
- spec/requests/user_subscriptions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"UserSubscriptions"` within the users domain.

### Behavioral Areas

- **UserSubscriptions**: Ensures correct behavior under the specified conditions
- **GET /user_subscriptions/subscribed - UserSubscriptions#subscribed**: Ensures correct behavior under the specified conditions
- **POST /user_subscriptions - UserSubscriptions#create**: Ensures correct behavior under the specified conditions
- **when rate limiting**: increments rate limit for user_subscription_creation

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/user_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/admin/gdpr_delete_requests_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: raises an error for missing params

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for missing params

### S-2: returns true if a user is already subscribed

- **Given** a user is already subscribed
- **When** the action is triggered
- **Then** returns true

### S-3: returns false if a user is not already subscribed

- **Given** a user is not already subscribed
- **When** the action is triggered
- **Then** returns false

### S-4: creates a UserSubscription

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a UserSubscription

### S-5: returns an error for an invalid source_type

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for an invalid source_type

### S-6: returns an error for a source that can

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for a source that can

### S-7: returns an error for an inactive source

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for an inactive source

### S-8: returns an error for a source that doesn

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for a source that doesn

### S-9: returns an error for an invalid UserSubscription

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for an invalid UserSubscription

### S-10: returns an error for an email mismatch

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for an email mismatch

### S-11: returns an error for a subscriber that signed up with Apple

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for a subscriber that signed up with Apple

### S-12: increments rate limit for user_subscription_creation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments rate limit for user_subscription_creation

