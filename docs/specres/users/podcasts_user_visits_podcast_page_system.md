---
id: "01KHY7Q02ABD5VT6PQX2R91AKG"
name: "podcasts_user_visits_podcast_page_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/delete_podcasts.rb
- spec/system/podcasts/user_visits_podcast_page_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User visits a podcast page**: displays podcast episodes

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: displays the header

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays the header

### S-2: displays podcast episodes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays podcast episodes

### S-3: displays podcast publish_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays podcast publish_at

### S-4: displays correct episodes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays correct episodes

