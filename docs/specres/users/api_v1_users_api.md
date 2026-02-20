---
id: "01KHY7PZWAZ48T8CSEFN0H0R7J"
name: "api_v1_users_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users_controller.rb
- app/helpers/admin/users_helper.rb
- app/helpers/users_helper.rb
- app/queries/admin/users_query.rb
- app/workers/spam/block_domain_and_suspend_users_worker.rb
- app/controllers/api/v1/user_roles_controller.rb
- spec/requests/api/v1/users_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::Users"` within the users domain.

### Behavioral Areas

- **Api::V1::Users**: Ensures correct behavior under the specified conditions
- **GET /api/users/:id**: Ensures correct behavior under the specified conditions
- **GET /api/users/me**: Ensures correct behavior under the specified conditions
- **when unauthenticated**: returns unauthenticated if no authentication and the Forem instance is set to private
- **when unauthorized**: returns unauthorized
- **when request is authenticated**: returns unauthenticated if no authentication and the Forem instance is set to private
- **GET /api/users/search**: Ensures correct behavior under the specified conditions
- **when unauthenticated**: returns unauthenticated if no authentication and the Forem instance is set to private

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/users_helper.rb` -- shared view utility methods
- **View helper**: `app/helpers/users_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/admin/users_query.rb` -- complex database query encapsulation
- **Background worker**: `app/workers/spam/block_domain_and_suspend_users_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns 404 if the user id is not found

- **Given** the user id is not found
- **When** the action is triggered
- **Then** returns 404

### S-2: returns 404 if the user username is not found

- **Given** the user username is not found
- **When** the action is triggered
- **Then** returns 404

### S-3: returns 404 if the user is not registered

- **Given** the user is not registered
- **When** the action is triggered
- **Then** returns 404

### S-4: returns 200 if the user username is found

- **Given** the user username is found
- **When** the action is triggered
- **Then** returns 200

### S-5: returns unauthenticated if no authentication and the Forem instance is set to pr...

- **Given** no authentication and the Forem instance is set to private
- **When** the action is triggered
- **Then** returns unauthenticated

### S-6: returns the correct json representation of the user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct json representation of the user

### S-7: includes email if display_email_on_profile is set to true

- **Given** display_email_on_profile is set to true
- **When** the action is triggered
- **Then** includes email

### S-8: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-9: includes badge_ids

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes badge_ids

### S-10: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-11: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-12: returns the correct json representation of the user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct json representation of the user

