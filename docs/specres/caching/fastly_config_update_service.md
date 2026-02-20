---
id: "01KHY7Q1H3A3EN4BAW25SCYDTC"
name: "fastly_config_update_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/fastly_config/update.rb
- app/errors/fastly_config.rb
- app/services/fastly_config/base.rb
- app/services/fastly_config/snippets.rb
- spec/services/fastly_config/update_spec.rb

## Functional Overview

This specification defines the expected behavior of `FastlyConfig::Update` within the caching domain.

### Behavioral Areas

- **::run**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/fastly_config/update.rb` -- business logic orchestration and domain operations
- `app/errors/fastly_config.rb`
- **Service layer**: `app/services/fastly_config/base.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/fastly_config/snippets.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: raises an error for incorrectly formatted configs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for incorrectly formatted configs

### S-2: raises an error for invalid configs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for invalid configs

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: updates Fastly if new updates are found

- **Given** new updates are found
- **When** the action is triggered
- **Then** updates Fastly

### S-5: logs success messages

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs success messages

