---
id: "01KHY7Q013TWBNNMDE7F1M3KZA"
name: "authentication_user_logs_in_with_twitter_system"
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
- spec/system/authentication/user_logs_in_with_twitter_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Authenticating` within the users domain.

### Behavioral Areas

- **Authenticating with Twitter**: creates a new user with a temporary username
- **when a user is new**: creates a new user
- **when using valid credentials**: Ensures correct behavior under the specified conditions
- **when trying to register with an already existing username**: creates a new user with a temporary username
- **when using invalid credentials**: Ensures correct behavior under the specified conditions
- **when a validation failure occurs**: Ensures correct behavior under the specified conditions
- **when a user already exists**: creates a new user
- **when using valid credentials**: Ensures correct behavior under the specified conditions

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

### S-2: logs in and redirects to the onboarding

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs in and redirects to the onboarding

### S-3: remembers the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** remembers the user

### S-4: creates a new user with a temporary username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new user with a temporary username

### S-5: does not create a new user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new user

### S-6: does not log in

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not log in

### S-7: notifies Datadog about a callback error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** notifies Datadog about a callback error

### S-8: notifies Datadog about an OAuth unauthorized error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** notifies Datadog about an OAuth unauthorized error

### S-9: notifies Datadog even with no OmniAuth error present

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** notifies Datadog even with no OmniAuth error present

### S-10: does not create a new user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new user

### S-11: redirects to the registration page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the registration page

### S-12: reports errors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** reports errors

