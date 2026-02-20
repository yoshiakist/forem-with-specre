---
id: "01KHY7PZSD4KYW0XMC7WJRQYD6"
name: "concerns_omniauth_redirect_controller"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/concerns/session_current_user.rb
- app/models/concerns/algolia_searchable/searchable_user.rb
- app/models/concerns/user_subscription_sourceable.rb
- spec/controllers/concerns/omniauth_redirect_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Omniauth` within the users domain.

### Behavioral Areas

- **Omniauth redirect**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/session_current_user.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/user_subscription_sourceable.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: avoids i=i param in after_sign_in_path_for

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** avoids i=i param in after_sign_in_path_for

### S-2: respects the origin param passed through the OAuth flow

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** respects the origin param passed through the OAuth flow

