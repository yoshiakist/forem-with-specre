---
id: "01KHY7PZZHWAW2SZD0TSD7VRNF"
name: "users_cancel_stripe_subscriptions_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/cancel_stripe_subscriptions.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/controllers/users_controller.rb
- spec/services/users/cancel_stripe_subscriptions_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::CancelStripeSubscriptions` within the users domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **when user has no stripe_id_code**: cancels all active Stripe subscriptions for the user
- **when user is nil**: cancels all active Stripe subscriptions for the user
- **when Stripe API returns an error**: cancels all active Stripe subscriptions for the user
- **when subscription cancellation fails**: cancels all active Stripe subscriptions for the user
- **when any other error occurs**: logs the error but does not raise it

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/cancel_stripe_subscriptions.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: cancels all active Stripe subscriptions for the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cancels all active Stripe subscriptions for the user

### S-2: logs successful cancellation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs successful cancellation

### S-3: does not attempt to cancel subscriptions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not attempt to cancel subscriptions

### S-4: does not attempt to cancel subscriptions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not attempt to cancel subscriptions

### S-5: logs the error but does not raise it

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the error but does not raise it

### S-6: logs the error but continues with other subscriptions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the error but continues with other subscriptions

### S-7: logs the error but does not raise it

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the error but does not raise it

