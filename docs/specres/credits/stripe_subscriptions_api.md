---
id: "01KHY7Q0RSFC1DRYCPEREAVVV2"
name: "stripe_subscriptions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/stripe_subscriptions_controller.rb
- app/services/users/cancel_stripe_subscriptions.rb
- spec/requests/stripe_subscriptions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"StripeSubscriptions"` within the credits domain.

### Behavioral Areas

- **StripeSubscriptions**: Ensures correct behavior under the specified conditions
- **GET /stripe_subscriptions/new**: Ensures correct behavior under the specified conditions
- **when the user is not signed in**: Ensures correct behavior under the specified conditions
- **when the user is signed in**: Ensures correct behavior under the specified conditions
- **when the user is a tag moderator**: uses the tag moderator item code
- **when the user is not a tag moderator**: uses the tag moderator item code
- **with custom parameters**: creates a Stripe Checkout Session with custom parameters
- **GET /stripe_subscriptions/edit**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/stripe_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/users/cancel_stripe_subscriptions.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: redirects to the sign in page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the sign in page

### S-2: uses the tag moderator item code

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the tag moderator item code

### S-3: uses the provided item code if it is different from the tag moderator item code

- **Given** it is different from the tag moderator item code
- **When** the action is triggered
- **Then** uses the provided item code

### S-4: falls back to the default item code if no valid item code is provided

- **Given** no valid item code is provided
- **When** the action is triggered
- **Then** falls back to the default item code

### S-5: allows other host redirection

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows other host redirection

### S-6: creates a Stripe Checkout Session with custom parameters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a Stripe Checkout Session with custom parameters

### S-7: redirects to the sign-in page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the sign-in page

### S-8: creates a Stripe Billing Portal session and redirects to it

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a Stripe Billing Portal session and redirects to it

### S-9: shows an error message and redirects back

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows an error message and redirects back

### S-10: redirects to the sign in page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the sign in page

### S-11: cancels the subscription and removes the base subscriber role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cancels the subscription and removes the base subscriber role

### S-12: does not cancel the subscription and shows an alert

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not cancel the subscription and shows an alert

