---
id: "01KHY7Q1HBMBT2D0FVQ0S87ZCF"
name: "mention_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/decorators/mention_decorator.rb
- app/models/mention.rb
- app/workers/notifications/mention_worker.rb
- spec/models/mention_spec.rb

## Functional Overview

This specification defines the expected behavior of `Mention` within the mentions domain.

### Behavioral Areas

- **.create_all**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions
- **when validating uniqueness of user_id**: allows the same user_id for different mentionable_id and mentionable_type
- **when mentionable is invalid**: is scoped to mentionable_id and mentionable_type
- **associations**: Ensures correct behavior under the specified conditions
- **callbacks**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Decorator**: `app/decorators/mention_decorator.rb` -- presentation logic and view-model enrichment
- **Model layer**: `app/models/mention.rb` -- data persistence, validations, and associations
- **Background worker**: `app/workers/notifications/mention_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of mentionable type
- belong to user
- belong to mentionable

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: enqueues a job to default queue

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues a job to default queue

### S-3: is scoped to mentionable_id and mentionable_type

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is scoped to mentionable_id and mentionable_type

### S-4: allows the same user_id for different mentionable_id and mentionable_type

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the same user_id for different mentionable_id and mentionable_type

### S-5: is invalid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid

### S-6: enqueues SendEmailNotificationWorker after create

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues SendEmailNotificationWorker after create

