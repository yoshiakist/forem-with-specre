---
id: "01KHY7Q0S5D5BCVDY9QN00B7SF"
name: "credits_sync_counter_cache_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/credits/sync_counter_cache.rb
- app/controllers/credits_controller.rb
- app/services/credits/buy.rb
- app/services/credits/ledger.rb
- app/services/credits/manage.rb
- spec/workers/credits/sync_counter_cache_spec.rb

## Functional Overview

This specification defines the expected behavior of `Credits::SyncCounterCache` within the credits domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/credits/sync_counter_cache.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/credits_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/credits/buy.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/credits/ledger.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/credits/manage.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: syncs counter cache for credits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** syncs counter cache for credits

