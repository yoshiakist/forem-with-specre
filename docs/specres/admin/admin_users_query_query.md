---
id: "01KHY7Q103GYCAG6SCP9340GH7"
name: "admin_users_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/queries/admin/users_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Admin::UsersQuery` within the admin domain.

### Behavioral Areas

- **.find**: Ensures correct behavior under the specified conditions
- **when identifier is blank**: Ensures correct behavior under the specified conditions
- **when identifier is an int id**: Ensures correct behavior under the specified conditions
- **when identifier is a string**: Ensures correct behavior under the specified conditions
- **when identifier is a username**: Ensures correct behavior under the specified conditions
- **when identifier is an email**: Ensures correct behavior under the specified conditions
- **.call**: Ensures correct behavior under the specified conditions
- **when no arguments are given**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- eq [user2, user]
- eq [user3]
- eq [user6]
- eq [user5, user2, user]
- eq [user5, user4]
- eq [user7, user5, user4]
- eq [user9, user8, user7, user6, user5, user4]
- eq [user10, user8]
- eq [user10, user5, user4]
- eq [user2, user]
- eq [user4]
- eq [user7]
- eq [user7]
- eq [user]
- eq [user]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: returns nil

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns nil

### S-3: returns user by id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user by id

### S-4: returns user by id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user by id

### S-5: returns user by id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user by id

### S-6: returns user by id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user by id

### S-7: returns all users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns all users

