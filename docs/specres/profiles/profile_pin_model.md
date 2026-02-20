---
id: "01KHY7Q0KGSRK8MQZJJ6XBZYGJ"
name: "profile_pin_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/profile_pins_controller.rb
- app/models/profile_pin.rb
- app/models/profile.rb
- app/models/profile_field.rb
- app/models/profile_field_group.rb
- spec/models/profile_pin_spec.rb

## Functional Overview

This specification defines the expected behavior of `ProfilePin` within the profiles domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **number of pins**: allows up to five pins per user
- **profile**: ensures pinnable belongs to the same profile

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/profile_pins_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/profile_pin.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile_field.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile_field_group.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: allows up to five pins per user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows up to five pins per user

### S-2: disallows the sixth pin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disallows the sixth pin

### S-3: ensures pinnable belongs to the same profile

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ensures pinnable belongs to the same profile

### S-4: ensures one pin per pinnable per profile

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ensures one pin per pinnable per profile

