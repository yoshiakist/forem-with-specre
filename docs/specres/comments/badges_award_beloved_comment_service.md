---
id: "01KHY7PZQMP3708MEHKQPTG5EK"
name: "badges_award_beloved_comment_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/badges/award_beloved_comment.rb
- spec/services/badges/award_beloved_comment_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badges::AwardBelovedComment` within the comments domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/badges/award_beloved_comment.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: awards beloved comment to folks who have a qualifying comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards beloved comment to folks who have a qualifying comment

### S-2: does not reward beloved comment to non-qualifying comment

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not reward beloved comment to non-qualifying comment

