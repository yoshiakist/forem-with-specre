---
id: "01KHY7PZX5VDD3W11RV1YRZF5X"
name: "user_user_show_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/admin/user_queries_controller.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/user_roles_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- spec/requests/user/user_show_spec.rb

## Functional Overview

This specification defines the expected behavior of `"UserShow"` within the users domain.

### Behavioral Areas

- **UserShow**: Ensures correct behavior under the specified conditions
- **GET /:slug (user)**: Ensures correct behavior under the specified conditions
- **when user signed in**: returns a 200 status when navigating to the user
- **when user not signed in**: returns a 200 status when navigating to the user
- **when user not signed in but internal nav triggered**: returns a 200 status when navigating to the user
- **GET /users/ID.json**: Ensures correct behavior under the specified conditions
- **when user not signed in**: returns a 200 status when navigating to the user
- **when user **is** signed in **and** trusted**: returns a 200 status when navigating to the user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/user_roles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns a 200 status when navigating to the user

- **Given** the system is in a standard operational state
- **When** navigating to the user
- **Then** returns a 200 status

### S-2: renders the proper JSON-LD for a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper JSON-LD for a user

### S-3: includes a subscription icon if user is subscribed

- **Given** user is subscribed
- **When** the action is triggered
- **Then** includes a subscription icon

### S-4: does not include a subscription icon if user is not subscribed

- **Given** user is not subscribed
- **When** the action is triggered
- **Then** does not include a subscription icon

### S-5: does not render a key if no value is given

- **Given** no value is given
- **When** the action is triggered
- **Then** does not render a key

### S-6: does not render json ld

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render json ld

### S-7: does not render json ld

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render json ld

### S-8: does not render json ld

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render json ld

### S-9: 404s when user not found

- **Given** the system is in a standard operational state
- **When** user not found
- **Then** 404s

### S-10: does not include 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include 

### S-11: **does** include 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** **does** include 

### S-12: redirects to the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the user

