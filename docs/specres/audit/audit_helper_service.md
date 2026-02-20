---
id: "01KHY7Q1HVSJYQZX2KS6XKGTZJ"
name: "audit_helper_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/audit/helper.rb
- app/models/audit_log.rb
- app/queries/audit_log/unpublish_alls_query.rb
- app/services/audit/event/payload.rb
- app/services/audit/logger.rb
- app/services/audit/notification.rb
- app/services/audit/subscribe.rb
- spec/services/audit/helper_spec.rb

## Functional Overview

This specification defines the expected behavior of `Audit::Helper` within the audit domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/audit/helper.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/audit_log.rb` -- data persistence, validations, and associations
- **Query object**: `app/queries/audit_log/unpublish_alls_query.rb` -- complex database query encapsulation
- **Service layer**: `app/services/audit/event/payload.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/audit/logger.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/audit/notification.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/audit/subscribe.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: has a notification suffix

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has a notification suffix

