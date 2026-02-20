---
id: "01KHY7Q1372YVNYXSP9MQEM55C"
name: "admin_scheduled_automations_controller_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/scheduled_automations_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `Admin::ScheduledAutomationsController` within the admin domain.

### Behavioral Areas

- **GET #index**: Ensures correct behavior under the specified conditions
- **GET #show**: Ensures correct behavior under the specified conditions
- **GET #new**: Ensures correct behavior under the specified conditions
- **POST #create**: Ensures correct behavior under the specified conditions
- **with valid parameters**: creates automation with correct next_run_at
- **with invalid parameters**: creates automation with correct next_run_at
- **with weekly frequency**: handles string values in frequency_config by normalizing them to integers
- **GET #edit**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: returns success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success

### S-2: assigns automations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns automations

### S-3: returns success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success

### S-4: returns success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success

### S-5: builds a new automation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** builds a new automation

### S-6: creates a new automation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new automation

### S-7: sets the next_run_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the next_run_at

### S-8: redirects to index

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to index

### S-9: sets a success flash message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets a success flash message

### S-10: handles string values in frequency_config by normalizing them to integers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles string values in frequency_config by normalizing them to integers

### S-11: does not create a new automation

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new automation

### S-12: renders new template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders new template

