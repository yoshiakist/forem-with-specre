---
id: "01KHY7Q1KGVR7VJXXRCKKZ9RN7"
name: "consumer_apps_rpush_app_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/consumer_apps/rpush_app_query.rb
- app/controllers/admin/consumer_apps_controller.rb
- app/queries/consumer_apps/find_or_create_all_query.rb
- app/queries/consumer_apps/find_or_create_by_query.rb
- spec/queries/consumer_apps/rpush_app_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `ConsumerApps::RpushAppQuery` within the consumer_apps domain.

### Behavioral Areas

- **Rpush app**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/consumer_apps/rpush_app_query.rb` -- complex database query encapsulation
- **Controller layer**: `app/controllers/admin/consumer_apps_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/consumer_apps/find_or_create_all_query.rb` -- complex database query encapsulation
- **Query object**: `app/queries/consumer_apps/find_or_create_by_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: is recreated after updating a ConsumerApp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is recreated after updating a ConsumerApp

### S-2: returns nil if ConsumerApp is not operational

- **Given** ConsumerApp is not operational
- **When** the action is triggered
- **Then** returns nil

### S-3: works when ConsumerApps have the same bundle but different platform

- **Given** the system is in a standard operational state
- **When** ConsumerApps have the same bundle but different platform
- **Then** works

