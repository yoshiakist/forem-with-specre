---
id: "01KHY7Q0ZES7J9Q4717Y819GW6"
name: "ahoy_tracking_create_account_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/ahoy/email_clicks_controller.rb
- app/models/ahoy/event.rb
- app/models/ahoy/visit.rb
- spec/system/ahoy/tracking_create_account_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Tracking` within the analytics domain.

### Behavioral Areas

- **Tracking**: has the necessary initial tracking elements
- **when on the homepage**: Ensures correct behavior under the specified conditions
- **when tracking through the modal**: has the necessary initial tracking elements

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/ahoy/email_clicks_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/ahoy/event.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/ahoy/visit.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: has the necessary initial tracking elements

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has the necessary initial tracking elements

### S-2: has the create account tracking element in the hamburger

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has the create account tracking element in the hamburger

### S-3: tracks a click with the correct source

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** tracks a click with the correct source

### S-4: adds an ahoy event

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds an ahoy event

