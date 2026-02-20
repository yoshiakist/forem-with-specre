---
id: "01KHY7Q0Q4DJ38NCZJMVHZV11A"
name: "feed_event_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/feed_events_controller.rb
- app/models/feed_event.rb
- app/models/feed_config.rb
- spec/models/feed_event_spec.rb

## Functional Overview

This specification defines the expected behavior of `FeedEvent` within the feeds domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **.record_journey_for**: Ensures correct behavior under the specified conditions
- **when the user**: updates the article counters and computes the score based on distinct impression users
- **when there are no feed events for the specified article**: creates a new feed event with attributes copied from the click
- **when the last click is not on the specified article**: creates a new feed event with attributes copied from the click
- **when the interaction type is not one of reaction, comment, or extended_pageview**: Ensures correct behavior under the specified conditions
- **after_create_commit .record_field_test_event**: Ensures correct behavior under the specified conditions
- **when experiments config is nil**: calculates and updates the feed config counters correctly

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/feed_events_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/feed_event.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/feed_config.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to article.optional
- validate numericality of article id.only integer
- belong to user.optional
- validate numericality of user id.only integer.allow nil
- define enum for category.with values valid categories
- validate numericality of article position.only integer.is greater than 0
- validate inclusion of context type.in array %w[home search tag email]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: creates a new feed event with attributes copied from the click

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new feed event with attributes copied from the click

### S-3: does not create a new feed event

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new feed event

### S-4: does not create a new feed event

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new feed event

### S-5: does not create a new feed event

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new feed event

### S-6: does not record a field test event

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not record a field test event

### S-7: updates the article counters and computes the score based on distinct impression...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the article counters and computes the score based on distinct impression users

### S-8: does not call update_single_article_counters

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call update_single_article_counters

### S-9: updates only the impressions count

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates only the impressions count

### S-10: sets the score based solely on the reaction multiplier

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the score based solely on the reaction multiplier

### S-11: counts duplicates for totals but uses distinct users for scoring

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts duplicates for totals but uses distinct users for scoring

### S-12: updates counters and scores for multiple articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates counters and scores for multiple articles

### S-13: leaves counters as zero

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** leaves counters as zero

