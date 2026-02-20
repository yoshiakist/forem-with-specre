---
id: "01KHY7PZTEZ5RYJNMKA31G999A"
name: "settings_authentication_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/authentications_controller.rb
- app/helpers/authentication_helper.rb
- app/lib/constants/settings/authentication.rb
- app/models/settings/authentication.rb
- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/lib/constants/settings/user_experience.rb
- app/models/settings/user_experience.rb
- app/services/settings/authentication/upsert.rb
- spec/models/settings/authentication_spec.rb

## Functional Overview

This specification defines the expected behavior of `Settings::Authentication` within the users domain.

### Behavioral Areas

- **acceptable_domain?**: Ensures correct behavior under the specified conditions
- **with blocked domain**: allows valid domain lists
- **when given a subdomain of a blocked domain**: allows valid domain lists
- **when the given domain has a suffix of the blocked domain**: allows valid domain lists
- **with allowed domain**: allows valid domain lists
- **with no domains blocked nor explicitly allowed**: Ensures correct behavior under the specified conditions
- **with no domains blocked but an explicitly allowed domain**: allows valid domain lists
- **validations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/authentication_helper.rb` -- shared view utility methods
- `app/lib/constants/settings/authentication.rb`
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- `app/lib/constants/settings/user_experience.rb`
- **Model layer**: `app/models/settings/user_experience.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/settings/authentication/upsert.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- be falsey
- be falsey
- be truthy
- be truthy
- be truthy
- be falsey

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: allows valid domain lists

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows valid domain lists

### S-3: rejects invalid domain lists

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid domain lists

### S-4: allows valid domain lists

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows valid domain lists

### S-5: rejects invalid domain lists

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid domain lists

