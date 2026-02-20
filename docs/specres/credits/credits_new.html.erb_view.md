---
id: "01KHY7Q0S3HKSFEQSAXR2JYNQ3"
name: "credits_new.html.erb_view"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/credits_controller.rb
- app/services/credits/buy.rb
- app/services/credits/ledger.rb
- app/services/credits/manage.rb
- app/workers/credits/sync_counter_cache.rb
- spec/views/credits/new.html.erb_spec.rb

## Functional Overview

This specification defines the expected behavior of `"credits/new"` within the credits domain.

### Behavioral Areas

- **credits/new**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/credits_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/credits/buy.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/credits/ledger.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/credits/manage.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/credits/sync_counter_cache.rb` -- asynchronous job processing


## Scenarios

### S-1: shows the page for light mode by default

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the page for light mode by default

### S-2: respects dark mode if set

- **Given** set
- **When** the action is triggered
- **Then** respects dark mode

### S-3: renders localized submitting message in js correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders localized submitting message in js correctly

