---
id: "01KHY7Q1B41A981FT1JV31Y5PY"
name: "middlewares_set_subforem_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/lib/middlewares/set_subforem.rb
- spec/lib/middlewares/set_subforem_spec.rb

## Functional Overview

This specification defines the expected behavior of `Middlewares::SetSubforem` within the subforems domain.

### Behavioral Areas

- **call**: Ensures correct behavior under the specified conditions
- **when a subforem exists for the requested domain**: sets subforem_id in RequestStore
- **when no subforem matches the requested domain**: sets subforem_id in RequestStore
- **when passed_domain parameter is provided**: uses the passed_domain parameter instead of the request host

### Implementation Architecture

The behavior is implemented across the following layers:

- `app/lib/middlewares/set_subforem.rb`


## Scenarios

### S-1: sets subforem_id in RequestStore

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets subforem_id in RequestStore

### S-2: sets subforem_domain in RequestStore from cached hash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets subforem_domain in RequestStore from cached hash

### S-3: sets default_subforem_id in RequestStore

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets default_subforem_id in RequestStore

### S-4: uses the cached id_to_domain_hash to set subforem_domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the cached id_to_domain_hash to set subforem_domain

### S-5: sets subforem_id to nil

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets subforem_id to nil

### S-6: does not set subforem_domain in RequestStore

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set subforem_domain in RequestStore

### S-7: still sets default_subforem_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** still sets default_subforem_id

### S-8: uses the passed_domain parameter instead of the request host

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the passed_domain parameter instead of the request host

