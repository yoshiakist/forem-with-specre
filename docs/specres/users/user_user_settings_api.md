---
id: "01KHY7PZX26J10W8KYTD0YMR9E"
name: "user_user_settings_api"
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
- spec/requests/user/user_settings_spec.rb

## Functional Overview

This specification defines the expected behavior of `"UserSettings"` within the users domain.

### Behavioral Areas

- **UserSettings**: Ensures correct behavior under the specified conditions
- **GET /settings/:tab**: Ensures correct behavior under the specified conditions
- **when not signed-in**: Ensures correct behavior under the specified conditions
- **when signed-in**: Ensures correct behavior under the specified conditions
- **:account**: Ensures correct behavior under the specified conditions
- **connect providers accounts**: does not allow to connect an Apple Account to an existing user
- **GitHub repositories**: renders the repositories container if the user has authenticated through GitHub
- **GET /settings/profile**: Ensures correct behavior under the specified conditions

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

### S-1: redirects them to login

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects them to login

### S-2: renders various settings tabs properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders various settings tabs properly

### S-3: handles unknown settings tab properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles unknown settings tab properly

### S-4: displays content on Profile tab properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays content on Profile tab properly

### S-5: displays profile groups content on Profile tab

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays profile groups content on Profile tab

### S-6: displays content on Customization tab properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays content on Customization tab properly

### S-7: displays content on Notifications tab properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays content on Notifications tab properly

### S-8: displays moderator notifications second on Notifications tab if trusted

- **Given** trusted
- **When** the action is triggered
- **Then** displays moderator notifications second on Notifications tab

### S-9: displays content on Account tab properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays content on Account tab properly

### S-10: displays content on Billing tab properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays content on Billing tab properly

### S-11: displays content on Organization tab properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays content on Organization tab properly

### S-12: displays content on Extensions tab properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays content on Extensions tab properly

