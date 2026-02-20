---
id: "01KHY7PZW7VKJ3DKM2WG9J3F00"
name: "api_v1_user_roles_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v1/user_roles_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- spec/requests/api/v1/user_roles_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::UserRoles"` within the users domain.

### Behavioral Areas

- **Api::V1::UserRoles**: Ensures correct behavior under the specified conditions
- **PUT /api/users/:id/suspend**: Ensures correct behavior under the specified conditions
- **when unauthenticated**: Ensures correct behavior under the specified conditions
- **when unauthorized**: returns unauthorized
- **when request is authenticated**: Ensures correct behavior under the specified conditions
- **PUT /api/users/:id/limited**: Ensures correct behavior under the specified conditions
- **when unauthenticated**: Ensures correct behavior under the specified conditions
- **when unauthorized**: returns unauthorized

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v1/user_roles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-2: returns unauthorized if api key is invalid

- **Given** api key is invalid
- **When** the action is triggered
- **Then** returns unauthorized

### S-3: returns unauthorized if api key belongs to non-admin user

- **Given** api key belongs to non-admin user
- **When** the action is triggered
- **Then** returns unauthorized

### S-4: is successful in suspending a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is successful in suspending a user

### S-5: creates an audit log of the action taken

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an audit log of the action taken

### S-6: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-7: returns unauthorized if api key is invalid

- **Given** api key is invalid
- **When** the action is triggered
- **Then** returns unauthorized

### S-8: returns unauthorized if api key belongs to non-admin user

- **Given** api key belongs to non-admin user
- **When** the action is triggered
- **Then** returns unauthorized

### S-9: is successful in limiting a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is successful in limiting a user

### S-10: creates an audit log of the action taken

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an audit log of the action taken

### S-11: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-12: returns unauthorized if api key is invalid

- **Given** api key is invalid
- **When** the action is triggered
- **Then** returns unauthorized

