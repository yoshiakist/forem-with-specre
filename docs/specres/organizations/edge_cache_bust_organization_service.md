---
id: "01KHY7Q0J9TYP6EQAJGX8TW76F"
name: "edge_cache_bust_organization_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust_organization.rb
- spec/services/edge_cache/bust_organization_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::BustOrganization` within the organizations domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/bust_organization.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: busts the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache

### S-2: logs an error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs an error

