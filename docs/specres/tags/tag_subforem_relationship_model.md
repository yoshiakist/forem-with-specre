---
id: "01KHY7Q0BJJQJY600EYT7PRNTG"
name: "tag_subforem_relationship_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/tag_subforem_relationship.rb
- app/models/tag_adjustment.rb
- spec/models/tag_subforem_relationship_spec.rb

## Functional Overview

This specification defines the expected behavior of `TagSubforemRelationship` within the tags domain.

### Behavioral Areas

- **associations**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions
- **database columns**: Ensures correct behavior under the specified conditions
- **uniqueness validation**: validates uniqueness of tag_id scoped to subforem_id

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/tag_subforem_relationship.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/tag_adjustment.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: validates uniqueness of tag_id scoped to subforem_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates uniqueness of tag_id scoped to subforem_id

### S-2: validates uniqueness of subforem_id scoped to tag_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates uniqueness of subforem_id scoped to tag_id

