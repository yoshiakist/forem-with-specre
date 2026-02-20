---
id: "01KHY7Q0Q1J2J0FWE9BW3SSJX4"
name: "feed_config_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/feed_config.rb
- app/models/feed_event.rb
- spec/models/feed_config_spec.rb

## Functional Overview

This specification defines the expected behavior of `FeedConfig` within the feeds domain.

### Behavioral Areas

- **score_sql**: Ensures correct behavior under the specified conditions
- **when tag_follow_weight is positive and tag count configs present**: invokes relevant_tags with configured counts and includes returned tags
- **when tag_follow_weight is positive but no tag count configs**: invokes relevant_tags with configured counts and includes returned tags
- **when all base weights are positive**: skips SQL terms for weights that are zero including labels and subforems
- **when some base weights are zero**: skips SQL terms for weights that are zero including labels and subforems
- **when all base weights are zero**: skips SQL terms for weights that are zero including labels and subforems
- **when additional weights are positive**: skips SQL terms for weights that are zero including labels and subforems
- **when recently active bonus is positive but user has no recent views**: falls back to user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/feed_config.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/feed_event.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: invokes relevant_tags with configured counts and includes returned tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** invokes relevant_tags with configured counts and includes returned tags

### S-2: falls back to user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to user

### S-3: includes all the expected SQL fragments including label and subforem matching

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes all the expected SQL fragments including label and subforem matching

### S-4: skips SQL terms for weights that are zero including labels and subforems

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** skips SQL terms for weights that are zero including labels and subforems

### S-5: returns 0 as the SQL expression

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 0 as the SQL expression

### S-6: includes the suppression for recently viewed articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the suppression for recently viewed articles

### S-7: includes the published today weight

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the published today weight

### S-8: includes the general past day bonus weight

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the general past day bonus weight

### S-9: includes the recently active past day bonus weight

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the recently active past day bonus weight

### S-10: includes the featured weight

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the featured weight

### S-11: includes the status weight

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the status weight

### S-12: includes the clickbait score subtraction

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the clickbait score subtraction

