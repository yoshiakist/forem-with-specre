---
id: "01KHY7Q1JAHN3MP6W64QXG9KDP"
name: "scheduled_automations_helper_helper"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/helpers/scheduled_automations_helper.rb
- spec/helpers/scheduled_automations_helper_spec.rb

## Functional Overview

This specification defines the expected behavior of `ScheduledAutomationsHelper` within the scheduled_automations domain.

### Behavioral Areas

- **format_frequency**: Ensures correct behavior under the specified conditions
- **with hourly frequency**: formats with integer values
- **with daily frequency**: formats with integer values
- **with weekly frequency**: formats with integer values
- **with custom_interval frequency**: formats with integer values
- **with unknown frequency**: formats with integer values
- **format_time**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **View helper**: `app/helpers/scheduled_automations_helper.rb` -- shared view utility methods


## Scenarios

### S-1: formats with integer values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** formats with integer values

### S-2: formats with string values (from form params)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** formats with string values (from form params)

### S-3: formats with integer values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** formats with integer values

### S-4: formats with string values (from form params)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** formats with string values (from form params)

### S-5: formats with integer values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** formats with integer values

### S-6: formats with string values (from form params)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** formats with string values (from form params)

### S-7: handles all days of the week correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles all days of the week correctly

### S-8: formats with integer values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** formats with integer values

### S-9: formats with string values (from form params)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** formats with string values (from form params)

### S-10: pluralizes 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** pluralizes 

### S-11: pluralizes 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** pluralizes 

### S-12: returns 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 

