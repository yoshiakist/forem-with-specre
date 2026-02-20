---
id: "01KHY7Q0C3H8Y6W2KWYM6HNAVM"
name: "ai_forem_tags_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/tags/moderators_controller.rb
- app/controllers/admin/tags_controller.rb
- app/controllers/api/v0/tags_controller.rb
- app/controllers/api/v1/tags_controller.rb
- app/controllers/concerns/api/tags_controller.rb
- app/controllers/liquid_tags_controller.rb
- spec/services/ai/forem_tags_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::ForemTags` within the tags domain.

### Behavioral Areas

- **upsert!**: Ensures correct behavior under the specified conditions
- **when AI call succeeds on first attempt**: retries and eventually succeeds
- **when AI call fails initially but succeeds on retry**: retries and eventually succeeds
- **when AI call fails all attempts**: logs warning messages for failed attempts
- **when AI response has invalid tags**: creates tags and relationships successfully
- **when AI response has too few valid tags**: creates tags and relationships successfully
- **when tag already exists without relationship**: creates tags and relationships successfully
- **when tag already exists with relationship and similar meaning**: creates tags and relationships successfully

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/tags/moderators_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates tags and relationships successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates tags and relationships successfully

### S-2: converts tag names to lowercase

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** converts tag names to lowercase

### S-3: retries and eventually succeeds

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retries and eventually succeeds

### S-4: logs warning messages for failed attempts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs warning messages for failed attempts

### S-5: logs error and returns without creating tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and returns without creating tags

### S-6: filters out invalid tags and only creates valid ones

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters out invalid tags and only creates valid ones

### S-7: logs warning and returns without creating tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs warning and returns without creating tags

### S-8: updates description and creates relationship

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates description and creates relationship

### S-9: skips the tag due to similar meaning

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** skips the tag due to similar meaning

### S-10: creates a new tag with different name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new tag with different name

### S-11: does not update existing description

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not update existing description

### S-12: logs error and continues processing

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and continues processing

