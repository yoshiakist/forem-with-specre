---
id: "01KHY7Q00B2B0W6BB2QY5G4N8S"
name: "authentication_conditional_registration_system"
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
- spec/system/authentication/conditional_registration_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Conditional` within the users domain.

### Behavioral Areas

- **Conditional registration (ForemWebView)**: Ensures correct behavior under the specified conditions
- **when browsing using mobile browser**: renders the social providers when all providers are enabled
- **when browsing using ForemWebView**: renders the social providers when all providers are enabled
- **when Apple Auth and email registration aren**: renders the social providers when all providers are enabled

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

### S-1: renders the social providers when all providers are enabled

- **Given** the system is in a standard operational state
- **When** all providers are enabled
- **Then** renders the social providers

### S-2: renders the social providers when all providers except Apple are enabled

- **Given** the system is in a standard operational state
- **When** all providers except Apple are enabled
- **Then** renders the social providers

### S-3: renders the social providers if Apple Auth is enabled

- **Given** Apple Auth is enabled
- **When** the action is triggered
- **Then** renders the social providers

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: renders the fallback message if Forem Auth is also disabled

- **Given** Forem Auth is also disabled
- **When** the action is triggered
- **Then** renders the fallback message

### S-6: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

