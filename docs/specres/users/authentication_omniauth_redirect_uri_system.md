---
id: "01KHY7Q00H2JPTMQRAA9K3G82N"
name: "authentication_omniauth_redirect_uri_system"
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
- spec/system/authentication/omniauth_redirect_uri_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Omniauth` within the users domain.

### Behavioral Areas

- **Omniauth redirect_uri**: Ensures correct behavior under the specified conditions

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

### S-1: relies on Settings::General.app_domain to generate correct callbacks_url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** relies on Settings::General.app_domain to generate correct callbacks_url

