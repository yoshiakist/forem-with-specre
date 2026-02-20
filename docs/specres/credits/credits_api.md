---
id: "01KHY7Q0RG9ASEA7N4QYMYQXQZ"
name: "credits_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/credits_controller.rb
- spec/requests/credits_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Credits"` within the credits domain.

### Behavioral Areas

- **Credits**: shows credits page
- **GET /credits**: Ensures correct behavior under the specified conditions
- **when the user has made purchases that will appear in the ledger**: shows credits page if user belongs to an org
- **POST credits**: shows credits page
- **when a user already has a card**: shows credits page if user belongs to an org
- **when purchasing as an organization**: creates unspent credits for the organization
- **when payment fails**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/credits_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: shows credits page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows credits page

### S-2: shows credits page if user belongs to an org

- **Given** user belongs to an org
- **When** the action is triggered
- **Then** shows credits page

### S-3: shows credits page if user belongs to an org and is org admin

- **Given** user belongs to an org and is org admin
- **When** the action is triggered
- **Then** shows credits page

### S-4: shows unattributed purchases

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows unattributed purchases

### S-5: creates unspent credits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates unspent credits

### S-6: makes a valid Stripe charge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** makes a valid Stripe charge

### S-7: makes a valid Stripe charge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** makes a valid Stripe charge

### S-8: creates unspent credits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates unspent credits

### S-9: charges a new card if given one

- **Given** given one
- **When** the action is triggered
- **Then** charges a new card

### S-10: creates unspent credits for the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates unspent credits for the organization

### S-11: makes a valid Stripe charge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** makes a valid Stripe charge

### S-12: does not create unspent credits for the current_user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create unspent credits for the current_user

