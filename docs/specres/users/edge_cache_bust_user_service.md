---
id: "01KHY7PZYAANHJZ17QJCZEYV2S"
name: "edge_cache_bust_user_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust_user.rb
- spec/services/edge_cache/bust_user_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::BustUser` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/bust_user.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: busts the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache

