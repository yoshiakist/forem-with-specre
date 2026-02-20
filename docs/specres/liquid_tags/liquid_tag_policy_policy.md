---
id: "01KHY7Q1ACHEMVACEZ9P44PH0H"
name: "liquid_tag_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/liquid_tag_policy.rb
- spec/policies/liquid_tag_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `LiquidTagPolicy` within the liquid_tags domain.

### Behavioral Areas

- **initialize?**: Ensures correct behavior under the specified conditions
- **when parsing a non-restricted tag without a user**: Ensures correct behavior under the specified conditions
- **when parsing a non-restricted tag with a user**: Ensures correct behavior under the specified conditions
- **when parsing a restricted tag without a user**: Ensures correct behavior under the specified conditions
- **when parsing a restricted tag with a user who **does not** meet the criteria**: Ensures correct behavior under the specified conditions
- **when parsing a restricted tag with a user who meets the criteria**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/liquid_tag_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: authorizes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** authorizes

### S-2: authorizes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** authorizes

### S-3: does not authorize

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not authorize

### S-4: does not authorize

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not authorize

### S-5: does not authorize

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not authorize

