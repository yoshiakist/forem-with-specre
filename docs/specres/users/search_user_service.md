---
id: "01KHY7PZYQ2J02R39ZW2M4FGJQ"
name: "search_user_service"
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
- app/controllers/concerns/session_current_user.rb
- app/controllers/user_blocks_controller.rb
- app/controllers/user_subscriptions_controller.rb
- app/controllers/users_controller.rb
- app/decorators/user_decorator.rb
- spec/services/search/user_spec.rb

## Functional Overview

This specification defines the expected behavior of `Search::User` within the users domain.

### Behavioral Areas

- **::search_documents**: Ensures correct behavior under the specified conditions
- **when describing the result format**: returns an empty result if there are no users
- **when searching for a term**: returns no items when out of pagination bounds
- **when sorting**: supports sorting by created_at in ascending and descending order
- **when paginating**: returns no items when out of pagination bounds

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
- **Controller layer**: `app/controllers/concerns/session_current_user.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/user_blocks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns an empty result if there are no users

- **Given** there are no users
- **When** the action is triggered
- **Then** returns an empty result

### S-2: does not return suspended users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return suspended users

### S-3: does not return unregistered (aka invited) users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return unregistered (aka invited) users

### S-4: returns regular users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns regular users

### S-5: returns admins

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns admins

### S-6: returns the correct attributes for a single result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct attributes for a single result

### S-7: matches against the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the user

### S-8: matches against the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the user

### S-9: sorts by 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sorts by 

### S-10: supports sorting by created_at in ascending and descending order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports sorting by created_at in ascending and descending order

### S-11: returns no items when out of pagination bounds

- **Given** the system is in a standard operational state
- **When** out of pagination bounds
- **Then** returns no items

### S-12: returns paginated items

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns paginated items

