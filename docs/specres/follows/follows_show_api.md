---
id: "01KHY7Q0PSRAJJDKQ27JVQRQFW"
name: "follows_show_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/followers_controller.rb
- app/controllers/api/v0/follows_controller.rb
- app/controllers/api/v1/followers_controller.rb
- app/controllers/api/v1/follows_controller.rb
- app/controllers/concerns/api/followers_controller.rb
- app/controllers/concerns/api/follows_controller.rb
- spec/requests/follows_show_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Follows` within the follows domain.

### Behavioral Areas

- **Follows #show**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: rejects unless logged-in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unless logged-in

### S-2: returns false when not following

- **Given** the system is in a standard operational state
- **When** not following
- **Then** returns false

### S-3: returns true when is following

- **Given** the system is in a standard operational state
- **When** is following
- **Then** returns true

### S-4: return self if current_user try to follow themself

- **Given** current_user try to follow themself
- **When** the action is triggered
- **Then** return self

### S-5: returns follow-back when current_user is followed by them

- **Given** the system is in a standard operational state
- **When** current_user is followed by them
- **Then** returns follow-back

### S-6: returns mutual when current_user is following them and they are following curren...

- **Given** the system is in a standard operational state
- **When** current_user is following them and they are following current_user
- **Then** returns mutual

