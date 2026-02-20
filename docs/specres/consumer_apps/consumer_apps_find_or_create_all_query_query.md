---
id: "01KHY7Q1KBX429X88QWHFH1JHG"
name: "consumer_apps_find_or_create_all_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/consumer_apps/find_or_create_all_query.rb
- app/controllers/admin/consumer_apps_controller.rb
- app/queries/consumer_apps/find_or_create_by_query.rb
- app/queries/consumer_apps/rpush_app_query.rb
- spec/queries/consumer_apps/find_or_create_all_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `ConsumerApps::FindOrCreateAllQuery` within the consumer_apps domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/consumer_apps/find_or_create_all_query.rb` -- complex database query encapsulation
- **Controller layer**: `app/controllers/admin/consumer_apps_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/consumer_apps/find_or_create_by_query.rb` -- complex database query encapsulation
- **Query object**: `app/queries/consumer_apps/rpush_app_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: fetches all ConsumerApp including the Forem apps

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fetches all ConsumerApp including the Forem apps

