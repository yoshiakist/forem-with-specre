---
id: "01KHY7PZZ26AEWME6KFDV8YHH0"
name: "settings_authentication_upsert_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/segmented_users/bulk_upsert.rb
- app/services/settings/authentication/upsert.rb
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
- spec/services/settings/authentication/upsert_spec.rb

## Functional Overview

This specification defines the expected behavior of `Settings::Authentication::Upsert` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/segmented_users/bulk_upsert.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/settings/authentication/upsert.rb` -- business logic orchestration and domain operations
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

### S-1: assigns enabled providers from parameters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns enabled providers from parameters

### S-2: disables providers that are not present

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disables providers that are not present

### S-3: does not save 1 or fewer providers when email_password login is not allowed

- **Given** the system is in a standard operational state
- **When** email_password login is not allowed
- **Then** does not save 1 or fewer providers

### S-4: will save with 1 or providers providers when email_password login is not allowed

- **Given** the system is in a standard operational state
- **When** email_password login is not allowed
- **Then** will save with 1 or providers providers

### S-5: disables providers even when provider parameter is blank

- **Given** the system is in a standard operational state
- **When** provider parameter is blank
- **Then** disables providers even

