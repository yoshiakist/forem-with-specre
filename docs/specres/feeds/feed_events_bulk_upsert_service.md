---
id: "01KHY7Q0QEFBBAJNX8Q3XFJXW6"
name: "feed_events_bulk_upsert_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/feed_events/bulk_upsert.rb
- app/controllers/feed_events_controller.rb
- spec/services/feed_events/bulk_upsert_spec.rb

## Functional Overview

This specification defines the expected behavior of `FeedEvents::BulkUpsert` within the feeds domain.

### Behavioral Areas

- **when there are no duplicates in the list or database**: Ensures correct behavior under the specified conditions
- **when there are more than 5 events**: inserts all the feed events
- **when there are duplicate events within the list**: inserts all the feed events
- **when there are invalid events in the list**: inserts all the feed events
- **when there is only one valid item in the list**: Ensures correct behavior under the specified conditions
- **when there are no valid items in the list**: Ensures correct behavior under the specified conditions
- **when there are already existing events with the same article, user and category**: inserts all the feed events

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/feed_events/bulk_upsert.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/feed_events_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: inserts all the feed events

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** inserts all the feed events

### S-2: calls bulk_update_counters_by_article_id for article ids

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls bulk_update_counters_by_article_id for article ids

### S-3: calls bulk_update_counters_by_article_id for article ids

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls bulk_update_counters_by_article_id for article ids

### S-4: does not insert extra duplicate events

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not insert extra duplicate events

### S-5: filters them out

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters them out

### S-6: handles it appropriately

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles it appropriately

### S-7: does nothing and returns

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does nothing and returns

### S-8: ignores them if no timebox is provided

- **Given** no timebox is provided
- **When** the action is triggered
- **Then** ignores them

### S-9: does not create new events if the existing matching events were created within t...

- **Given** the existing matching events were created within the provided timebox
- **When** the action is triggered
- **Then** does not create new events

### S-10: creates new events if the existing matching events were created outside the prov...

- **Given** the existing matching events were created outside the provided timebox
- **When** the action is triggered
- **Then** creates new events

