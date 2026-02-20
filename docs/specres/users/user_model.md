---
id: "01KHY7PZV7F0FD1E65TP9F4DH5"
name: "user_model"
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
- spec/models/user_spec.rb

## Functional Overview

This specification defines the expected behavior of `User` within the users domain.

### Behavioral Areas

- **delegations**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **when evaluating the custom error message for username uniqueness**: renders custom error message with value of taken username
- **when callbacks are triggered before validation**: sends a setup welcome notification when an active broadcast exists
- **email**: validates can_send_confirmation_email for existing user
- **username**: renders custom error message with value of taken username
- **when callbacks are triggered before and after create**: sends a setup welcome notification when an active broadcast exists

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

### S-1: Data integrity and associations

The model enforces the following constraints:

- delegate method admin?.to authorizer
- delegate method any admin?.to authorizer
- delegate method auditable?.to authorizer
- delegate method banished?.to authorizer
- delegate method comment suspended?.to authorizer
- delegate method creator?.to authorizer
- delegate method has trusted role?.to authorizer
- delegate method podcast admin for?.to authorizer
- delegate method restricted liquid tag for?.to authorizer
- delegate method single resource admin for?.to authorizer
- delegate method super admin?.to authorizer
- delegate method support admin?.to authorizer
- delegate method suspended?.to authorizer
- delegate method spam?.to authorizer
- delegate method spam or suspended?.to authorizer

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: renders custom error message with value of taken username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders custom error message with value of taken username

### S-3: validates username against reserved words

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates username against reserved words

### S-4: takes organization slug into account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** takes organization slug into account

### S-5: takes podcast slug into account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** takes podcast slug into account

### S-6: takes page slug into account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** takes page slug into account

### S-7: validates can_send_confirmation_email for existing user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates can_send_confirmation_email for existing user

### S-8: validates update_rate_limit for existing user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates update_rate_limit for existing user

### S-9: sets #{username_field} to nil if empty

- **Given** empty
- **When** the action is triggered
- **Then** sets #{username_field} to nil

### S-10: does not change a valid name

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not change a valid name

### S-11: sets email to nil if empty

- **Given** empty
- **When** the action is triggered
- **Then** sets email to nil

### S-12: does not change a valid name

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not change a valid name

### S-13: receives a generated username if none is given

- **Given** none is given
- **When** the action is triggered
- **Then** receives a generated username

