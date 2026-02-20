---
id: "01KHY7Q1H17C4RGP51BC1GFFGT"
name: "fastly_config_snippets_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/fastly_config/snippets.rb
- app/errors/fastly_config.rb
- app/services/fastly_config/base.rb
- app/services/fastly_config/update.rb
- spec/services/fastly_config/snippets_spec.rb

## Functional Overview

This specification defines the expected behavior of `FastlyConfig::Snippets` within the caching domain.

### Behavioral Areas

- **upsert_config**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/fastly_config/snippets.rb` -- business logic orchestration and domain operations
- `app/errors/fastly_config.rb`
- **Service layer**: `app/services/fastly_config/base.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/fastly_config/update.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: determines if an update is needed

- **Given** an update is needed
- **When** the action is triggered
- **Then** determines

### S-2: creates a new snippet if one isn

- **Given** one isn
- **When** the action is triggered
- **Then** creates a new snippet

### S-3: updates a snippet if one is found

- **Given** one is found
- **When** the action is triggered
- **Then** updates a snippet

### S-4: logs success messages

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs success messages

