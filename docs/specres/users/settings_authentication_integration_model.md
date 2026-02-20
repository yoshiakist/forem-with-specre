---
id: "01KHY7PZTC0CZ3EVGCKTWBXY8R"
name: "settings_authentication_integration_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/authentications_controller.rb
- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/lib/constants/settings/authentication.rb
- app/lib/constants/settings/user_experience.rb
- app/models/settings/authentication.rb
- app/models/settings/user_experience.rb
- app/services/settings/authentication/upsert.rb
- spec/models/settings/authentication_integration_spec.rb

## Functional Overview

This specification defines the expected behavior of `"BlockedEmailDomain` within the users domain.

### Behavioral Areas

- **BlockedEmailDomain Integration**: Ensures correct behavior under the specified conditions
- **Settings::Authentication.acceptable_domain?**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- `app/lib/constants/settings/authentication.rb`
- `app/lib/constants/settings/user_experience.rb`
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/user_experience.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/settings/authentication/upsert.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: blocks domains from both the old setting and the new model

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks domains from both the old setting and the new model

