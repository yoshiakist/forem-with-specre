---
id: "01KHY7Q0RBXTKDG0EV3MCKJ3MA"
name: "credit_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/credits_controller.rb
- app/models/credit.rb
- app/services/payments/process_credit_purchase.rb
- spec/models/credit_spec.rb

## Functional Overview

This specification defines the expected behavior of `Credit` within the credits domain.

### Behavioral Areas

- **when caching counters**: Ensures correct behavior under the specified conditions
- **credits_count**: Ensures correct behavior under the specified conditions
- **unspent_credits_count**: Ensures correct behavior under the specified conditions
- **spent_credits_count**: Ensures correct behavior under the specified conditions
- **purchase**: is valid without a purchase
- **add_to**: Ensures correct behavior under the specified conditions
- **remove_from**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/credits_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/credit.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/payments/process_credit_purchase.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user.optional
- belong to organization.optional
- belong to purchase.optional

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: counts credits for user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts credits for user

### S-3: counts credits for organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts credits for organization

### S-4: counts the number of unspent credits for a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts the number of unspent credits for a user

### S-5: counts the number of unspent credits for an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts the number of unspent credits for an organization

### S-6: counts the number of spent credits for a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts the number of spent credits for a user

### S-7: counts the number of spent credits for an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts the number of spent credits for an organization

### S-8: is valid without a purchase

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid without a purchase

### S-9: adds the credits to the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the credits to the user

### S-10: adds the credits to the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the credits to the organization

### S-11: adds the credits to the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the credits to the user

### S-12: adds the credits to the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the credits to the organization

