---
id: "01KHY7Q1H6WJM97RF15T67VMX8"
name: "fastly_task"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/errors/fastly_config.rb
- app/services/edge_cache/bust/fastly.rb
- spec/tasks/fastly_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Fastly` within the caching domain.

### Behavioral Areas

- **Fastly tasks**: does run if Fastly is configured
- **update_configs**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- `app/errors/fastly_config.rb`
- **Service layer**: `app/services/edge_cache/bust/fastly.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-3: does run if Fastly is configured

- **Given** Fastly is configured
- **When** the action is triggered
- **Then** does run

