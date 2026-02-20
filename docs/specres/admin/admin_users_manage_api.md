---
id: "01KHY7Q143NFSZ0XH0P23VK2TQ"
name: "admin_users_manage_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/users_manage_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin::Users"` within the admin domain.

### Behavioral Areas

- **Admin::Users**: Ensures correct behavior under the specified conditions
- **when merging users**: selects super admin role when user was suspended
- **when managing activity and roles**: selects super admin role when user was suspended
- **when adding tag moderator role**: adds comment suspend role
- **when deleting user**: deletes duplicate user
- **when handling credits**: selects super admin role when user was suspended


## Scenarios

### S-1: deletes duplicate user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes duplicate user

### S-2: merges all content

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** merges all content

### S-3: merges all relationships

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** merges all relationships

### S-4: merges misc profile info

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** merges misc profile info

### S-5: merges social identities and usernames

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** merges social identities and usernames

### S-6: merges an identity on a single account into the other

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** merges an identity on a single account into the other

### S-7: adds comment suspend role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds comment suspend role

### S-8: adds limited role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds limited role

### S-9: selects new role for user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** selects new role for user

### S-10: selects super admin role when user was suspended

- **Given** the system is in a standard operational state
- **When** user was suspended
- **Then** selects super admin role

### S-11: does not allow non-super-admin to doll out admin

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow non-super-admin to doll out admin

### S-12: creates a general note on the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a general note on the user

