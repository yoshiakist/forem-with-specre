---
id: "01KHY7Q10BJWRXTBSG7KGZ4JAE"
name: "admin_badge_automations_controller_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/badge_automations_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `Admin::BadgeAutomationsController` within the admin domain.

### Behavioral Areas

- **GET #index**: Ensures correct behavior under the specified conditions
- **GET #new**: Ensures correct behavior under the specified conditions
- **POST #create**: Ensures correct behavior under the specified conditions
- **with valid parameters**: builds a new automation with correct defaults
- **with invalid parameters**: builds a new automation with correct defaults
- **with different frequency types**: builds a new automation with correct defaults
- **GET #edit**: Ensures correct behavior under the specified conditions
- **PATCH #update**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: returns success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success

### S-2: assigns the badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns the badge

### S-3: lists automations for the badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists automations for the badge

### S-4: only shows automations for this specific badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only shows automations for this specific badge

### S-5: returns success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success

### S-6: assigns the badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns the badge

### S-7: builds a new automation with correct defaults

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** builds a new automation with correct defaults

### S-8: assigns organizations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns organizations

### S-9: creates a new automation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new automation

### S-10: assigns the current user as the automation user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns the current user as the automation user

### S-11: sets the correct action and service_name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the correct action and service_name

### S-12: sets the badge_slug in action_config

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the badge_slug in action_config

