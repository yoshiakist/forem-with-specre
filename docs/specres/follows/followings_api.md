---
id: "01KHY7Q0PEQDEPCNHKE9YKYEYB"
name: "followings_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/followings_controller.rb
- spec/requests/followings_spec.rb

## Functional Overview

This specification defines the expected behavior of `"FollowingsController"` within the follows domain.

### Behavioral Areas

- **FollowingsController**: Ensures correct behavior under the specified conditions
- **GET /followings/users**: Ensures correct behavior under the specified conditions
- **when user is unauthorized**: returns unauthorized
- **when user is authorized**: returns unauthorized
- **GET /followings/tags**: Ensures correct behavior under the specified conditions
- **when user is unauthorized**: returns unauthorized
- **when user is authorized**: returns unauthorized
- **GET /followings/organizations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/followings_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-2: returns user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user

### S-3: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-4: returns the user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the user

### S-5: returns the user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the user

### S-6: returns a list with the correct format

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a list with the correct format

### S-7: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-8: returns user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user

### S-9: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-10: returns user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user

