---
id: "01KHY7Q0RYRHJZAXJ66QQKQ8Y6"
name: "payments_customer_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/payments/customer.rb
- app/errors/payments.rb
- app/services/payments/process_credit_purchase.rb
- spec/services/payments/customer_spec.rb

## Functional Overview

This specification defines the expected behavior of `Payments::Customer` within the credits domain.

### Behavioral Areas

- **.get**: Ensures correct behavior under the specified conditions
- **.create**: Ensures correct behavior under the specified conditions
- **.create_source**: Ensures correct behavior under the specified conditions
- **.get_source**: Ensures correct behavior under the specified conditions
- **.detach_source**: Ensures correct behavior under the specified conditions
- **.charge**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/payments/customer.rb` -- business logic orchestration and domain operations
- `app/errors/payments.rb`
- **Service layer**: `app/services/payments/process_credit_purchase.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: retrieves an existing customer

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retrieves an existing customer

### S-2: raises Payments::CustomerNotFoundError if the customer does not exist

- **Given** the customer does not exist
- **When** the action is triggered
- **Then** raises Payments::CustomerNotFoundError

### S-3: increments stripe.errors if the customer does not exist

- **Given** the customer does not exist
- **When** the action is triggered
- **Then** increments stripe.errors

### S-4: raises Payments::PaymentsError for any other known error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises Payments::PaymentsError for any other known error

### S-5: increments stripe.errors for any other known error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments stripe.errors for any other known error

### S-6: creates a new customer

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new customer

### S-7: raises an error if anything in the params is invalid

- **Given** anything in the params is invalid
- **When** the action is triggered
- **Then** raises an error

### S-8: raises Payments::PaymentsError for any other known error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises Payments::PaymentsError for any other known error

### S-9: creates a new source

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new source

### S-10: raises an error if anything in the params is invalid

- **Given** anything in the params is invalid
- **When** the action is triggered
- **Then** raises an error

### S-11: increments stripe.errors if anything in the params is invalid

- **Given** anything in the params is invalid
- **When** the action is triggered
- **Then** increments stripe.errors

### S-12: raises Payments::PaymentsError for any other known error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises Payments::PaymentsError for any other known error

