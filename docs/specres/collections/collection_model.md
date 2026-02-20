---
id: "01KHY7Q1C21BZJD63AC59HEX8R"
name: "collection_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/collections_controller.rb
- app/models/collection.rb
- spec/models/collection_spec.rb

## Functional Overview

This specification defines the expected behavior of `Collection` within the collections domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **slug uniqueness**: enforces uniqueness within user_id
- **for personal collections (no organization)**: Ensures correct behavior under the specified conditions
- **for organization collections**: enforces uniqueness within organization_id (not user_id)
- **.find_series**: Ensures correct behavior under the specified conditions
- **with organization**: enforces uniqueness within user_id
- **path**: returns the correct path
- **when callbacks are triggered after touch**: returns an existing series for an organization when called by the same user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/collections_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/collection.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user
- belong to organization.optional
- have many articles.dependent nullify
- validate presence of slug

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: enforces uniqueness within user_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enforces uniqueness within user_id

### S-3: allows same slug for different users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows same slug for different users

### S-4: enforces uniqueness within organization_id (not user_id)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enforces uniqueness within organization_id (not user_id)

### S-5: allows same slug for different organizations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows same slug for different organizations

### S-6: returns an existing series

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an existing series

### S-7: creates a new series for a user if an existing one is not found

- **Given** an existing one is not found
- **When** the action is triggered
- **Then** creates a new series for a user

### S-8: creates a new series with an existing slug for a new user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new series with an existing slug for a new user

### S-9: creates a new series for an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new series for an organization

### S-10: returns an existing series for an organization regardless of user_id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an existing series for an organization regardless of user_id

### S-11: returns an existing series for an organization when called by the same user

- **Given** the system is in a standard operational state
- **When** called by the same user
- **Then** returns an existing series for an organization

### S-12: allows same slug for different organizations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows same slug for different organizations

### S-13: returns the correct path

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct path

