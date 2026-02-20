---
id: "01KHY7Q0RPG6Z9STZRA0Y5EM6C"
name: "stripe_active_cards_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/stripe_active_cards_controller.rb
- spec/requests/stripe_active_cards_spec.rb

## Functional Overview

This specification defines the expected behavior of `"StripeActiveCards"` within the credits domain.

### Behavioral Areas

- **StripeActiveCards**: Ensures correct behavior under the specified conditions
- **POST /stripe_active_cards**: Ensures correct behavior under the specified conditions
- **PUT /stripe_active_cards/:card_id**: Ensures correct behavior under the specified conditions
- **DELETE /stripe_active_cards/:card_id**: successfully deletes the card from sources
- **when a valid request is made**: Ensures correct behavior under the specified conditions
- **when an invalid request is made**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/stripe_active_cards_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: successfully adds a card to the correct user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** successfully adds a card to the correct user

### S-2: creates an AuditLog entry for successful creates

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an AuditLog entry for successful creates

### S-3: does not add a card if there is a card error

- **Given** there is a card error
- **When** the action is triggered
- **Then** does not add a card

### S-4: increments sidekiq.errors in Datadog on failure

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments sidekiq.errors in Datadog on failure

### S-5: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-6: increments sidekiq.errors.new_subscription in Datadog on failure

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments sidekiq.errors.new_subscription in Datadog on failure

### S-7: updates the customer default source

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the customer default source

### S-8: creates an AuditLog entry for successful updates

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an AuditLog entry for successful updates

### S-9: does not update the customer default souce if the source ID is unknown

- **Given** the source ID is unknown
- **When** the action is triggered
- **Then** does not update the customer default souce

### S-10: increments sidekiq.errors in Datadog on failure

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments sidekiq.errors in Datadog on failure

### S-11: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-12: increments sidekiq.errors.update_subscription in Datadog on failure

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments sidekiq.errors.update_subscription in Datadog on failure

