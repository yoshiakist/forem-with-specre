---
id: "01KHY7Q00RMC3D4BE13YK1DPBB"
name: "authentication_user_logs_in_with_email_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/authentications_controller.rb
- app/errors/authentication/errors.rb
- app/helpers/authentication_helper.rb
- app/lib/constants/settings/authentication.rb
- app/models/settings/authentication.rb
- app/services/authentication/authenticator.rb
- app/services/authentication/paths.rb
- app/services/authentication/providers.rb
- app/services/authentication/providers/apple.rb
- app/services/authentication/providers/facebook.rb
- spec/system/authentication/user_logs_in_with_email_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Authenticating` within the users domain.

### Behavioral Areas

- **Authenticating with Email**: logs in and redirects to email confirmation
- **when a user is new**: creates a new user
- **when using valid credentials**: Ensures correct behavior under the specified conditions
- **when trying to register with an already existing email**: logs in and redirects to email confirmation
- **when using invalid credentials**: Ensures correct behavior under the specified conditions
- **when a user already exists**: creates a new user
- **when using valid credentials**: Ensures correct behavior under the specified conditions
- **when already signed in**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- `app/errors/authentication/errors.rb`
- **View helper**: `app/helpers/authentication_helper.rb` -- shared view utility methods
- `app/lib/constants/settings/authentication.rb`
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/authentication/authenticator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/paths.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/apple.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/facebook.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: creates a new user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new user

### S-2: logs in and redirects to email confirmation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs in and redirects to email confirmation

### S-3: displays the properly decoded email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays the properly decoded email

### S-4: shows an error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows an error

### S-5: does not log in

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not log in

### S-6: logs in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs in

### S-7: logs in and redirects to onboarding if it hasn

- **Given** it hasn
- **When** the action is triggered
- **Then** logs in and redirects to onboarding

### S-8: redirects to the feed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the feed

### S-9: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-10: does not let malicious users enumerate email addresses

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not let malicious users enumerate email addresses

