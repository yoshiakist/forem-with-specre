---
id: "01KHY7PZVQR0AZ99XFWEGX88NG"
name: "users_suspended_username_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/users/suspended_username.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/controllers/users_controller.rb
- spec/models/users/suspended_username_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::SuspendedUsername` within the users domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **.previously_suspended?**: Ensures correct behavior under the specified conditions
- **.create_from_user**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/users/suspended_username.rb` -- data persistence, validations, and associations
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of username hash
- validate uniqueness of username hash

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: returns true if the user has been previously suspended

- **Given** the user has been previously suspended
- **When** the action is triggered
- **Then** returns true

### S-3: returns true if the user has been previously assigned a spam roles

- **Given** the user has been previously assigned a spam roles
- **When** the action is triggered
- **Then** returns true

### S-4: returns false if the user has not been previously_suspended

- **Given** the user has not been previously_suspended
- **When** the action is triggered
- **Then** returns false

### S-5: records a hash of the username in the database

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records a hash of the username in the database

