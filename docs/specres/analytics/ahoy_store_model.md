---
id: "01KHY7Q0YP3CSRCFEKG63JSCM1"
name: "ahoy_store_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/ahoy/email_clicks_controller.rb
- app/models/ahoy/event.rb
- app/models/ahoy/visit.rb
- spec/models/ahoy/store_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ahoy::Store` within the analytics domain.

### Behavioral Areas

- **track_visit**: Ensures correct behavior under the specified conditions
- **when context is not found**: creates a new UserVisitContext and increments visit count
- **when context is found**: creates a new UserVisitContext and increments visit count

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/ahoy/email_clicks_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/ahoy/event.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/ahoy/visit.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: creates a new UserVisitContext and increments visit count

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new UserVisitContext and increments visit count

### S-2: increments the visit count

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments the visit count

### S-3: updates the last_visit_at timestamp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the last_visit_at timestamp

### S-4: calls super with the correct data including context id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls super with the correct data including context id

