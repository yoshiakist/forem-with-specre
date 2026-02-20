---
id: "01KHY7PZXRQNACP6Q9J5S1WTV8"
name: "authentication_authenticator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/authentication/authenticator.rb
- app/controllers/admin/settings/authentications_controller.rb
- app/errors/authentication/errors.rb
- app/helpers/authentication_helper.rb
- app/lib/constants/settings/authentication.rb
- app/models/settings/authentication.rb
- app/services/authentication/paths.rb
- app/services/authentication/providers.rb
- app/services/authentication/providers/apple.rb
- app/services/authentication/providers/facebook.rb
- app/services/authentication/providers/forem.rb
- spec/services/authentication/authenticator_spec.rb

## Functional Overview

This specification defines the expected behavior of `Authentication::Authenticator` within the users domain.

### Behavioral Areas

- **when email is spammy**: avoids overriding the email when a provider has a different one
- **when new user status admin setting is limited**: does not make any changes to roles if the user already exists
- **when authenticating through an unknown provider**: raises ProviderNotFound
- **when authenticating through Apple**: avoids overriding the email when a provider has a different one
- **spam handling**: raises an Identity::SpamDomainForIdentityError
- **appropriate new user status**: does not make any changes to roles if the user already exists
- **new user**: does not make any changes to roles if the user already exists
- **existing user**: does not make any changes to roles if the user already exists

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/authentication/authenticator.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- `app/errors/authentication/errors.rb`
- **View helper**: `app/helpers/authentication_helper.rb` -- shared view utility methods
- `app/lib/constants/settings/authentication.rb`
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/authentication/paths.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/apple.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/facebook.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/forem.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: raises an Identity::SpamDomainForIdentityError

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an Identity::SpamDomainForIdentityError

### S-2: does not make any changes to roles if the user already exists

- **Given** the user already exists
- **When** the action is triggered
- **Then** does not make any changes to roles

### S-3: registers a user in good standing by default

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** registers a user in good standing by default

### S-4: registers the user as limited

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** registers the user as limited

### S-5: raises ProviderNotFound

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises ProviderNotFound

### S-6: creates a new user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new user

### S-7: creates a new identity

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new identity

### S-8: extracts the proper data from the auth payload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** extracts the proper data from the auth payload

### S-9: sets default fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets default fields

### S-10: sets the correct sign up cta variant

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the correct sign up cta variant

### S-11: sets remember_me for the new user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets remember_me for the new user

### S-12: queues a slack message to be sent for a user whose identity is brand new

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** queues a slack message to be sent for a user whose identity is brand new

