---
id: "01KHY7Q0M0Y3PSADF2HGTCGFBY"
name: "profile_preview_cards_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/profile_preview_cards_controller.rb
- spec/requests/profile_preview_cards_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ProfilePreviewCards"` within the profiles domain.

### Behavioral Areas

- **ProfilePreviewCards**: Ensures correct behavior under the specified conditions
- **GET /:id**: Ensures correct behavior under the specified conditions
- **when signed out**: Ensures correct behavior under the specified conditions
- **when signed in**: Ensures correct behavior under the specified conditions
- **GET /:id as JSON**: Ensures correct behavior under the specified conditions
- **when signed out**: Ensures correct behavior under the specified conditions
- **when signed in**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/profile_preview_cards_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: does not find an unknown user id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not find an unknown user id

### S-2: is a successful response

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is a successful response

### S-3: returns the data

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the data

### S-4: does not find an unknown user id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not find an unknown user id

### S-5: is a successful response

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is a successful response

### S-6: returns the data

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the data

### S-7: does not find an unknown user id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not find an unknown user id

### S-8: is a successful response

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is a successful response

### S-9: returns the data

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the data

### S-10: has the correct card color

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has the correct card color

### S-11: does not return the email if the user has asked not to

- **Given** the user has asked not to
- **When** the action is triggered
- **Then** does not return the email

### S-12: returns the email if the user wants to

- **Given** the user wants to
- **When** the action is triggered
- **Then** returns the email

