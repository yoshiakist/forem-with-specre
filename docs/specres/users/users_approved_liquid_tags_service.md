---
id: "01KHY7PZZFYH3WX69XX7PMVYP4"
name: "users_approved_liquid_tags_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/approved_liquid_tags.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/controllers/users_controller.rb
- spec/services/users/approved_liquid_tags_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::ApprovedLiquidTags` within the users domain.

### Behavioral Areas

- **when user is admin**: Ensures correct behavior under the specified conditions
- **when user has no role**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/approved_liquid_tags.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- match [UserSubscriptionTag]
- be empty

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

