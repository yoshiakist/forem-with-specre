---
id: "01KHY7Q0RKZW9VBW2A4XWKA4P6"
name: "incoming_webhooks_stripe_stripe_events_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/incoming_webhooks/stripe_events_controller.rb
- app/controllers/stripe_active_cards_controller.rb
- app/controllers/stripe_subscriptions_controller.rb
- app/policies/stripe_active_card_policy.rb
- app/policies/stripe_subscription_policy.rb
- app/services/users/cancel_stripe_subscriptions.rb
- spec/requests/incoming_webhooks/stripe/stripe_events_spec.rb

## Functional Overview

This specification defines the expected behavior of `"IncomingWebhooks::StripeEventsController"` within the credits domain.

### Behavioral Areas

- **IncomingWebhooks::StripeEventsController**: Ensures correct behavior under the specified conditions
- **POST /incoming_webhooks/stripe_events**: Ensures correct behavior under the specified conditions
- **when checkout.session.completed**: skips conversion when the click is too old
- **with a customer id present**: Ensures correct behavior under the specified conditions
- **when customer.subscription.updated**: skips conversion when the click is too old
- **and cancel_at_period_end is true**: Ensures correct behavior under the specified conditions
- **and cancel_at_period_end is false**: Ensures correct behavior under the specified conditions
- **when customer.subscription.deleted**: skips conversion when the click is too old

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/incoming_webhooks/stripe_events_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stripe_active_cards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stripe_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Policy layer**: `app/policies/stripe_active_card_policy.rb` -- authorization and access control rules
- **Policy layer**: `app/policies/stripe_subscription_policy.rb` -- authorization and access control rules
- **Service layer**: `app/services/users/cancel_stripe_subscriptions.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns status :ok

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns status :ok

### S-2: grants the base_subscriber role and sets status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** grants the base_subscriber role and sets status

### S-3: creates a conversion BillboardEvent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a conversion BillboardEvent

### S-4: sends the subscriber role email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the subscriber role email

### S-5: skips conversion when the click is too old

- **Given** the system is in a standard operational state
- **When** the click is too old
- **Then** skips conversion

### S-6: stores stripe_id_code on the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stores stripe_id_code on the user

### S-7: adds the impending_base_subscriber_cancellation role and updates status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the impending_base_subscriber_cancellation role and updates status

### S-8: ensures the user has only the base_subscriber role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ensures the user has only the base_subscriber role

### S-9: adds the impending_base_subscriber_cancellation role and updates status to not_s...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the impending_base_subscriber_cancellation role and updates status to not_subscribed

