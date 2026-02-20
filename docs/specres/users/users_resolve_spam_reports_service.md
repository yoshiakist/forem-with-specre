---
id: "01KHY7Q0017FTTV0NRRZS56RMK"
name: "users_resolve_spam_reports_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/resolve_spam_reports.rb
- app/workers/users/resolve_spam_reports_worker.rb
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
- spec/services/users/resolve_spam_reports_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::ResolveSpamReports` within the users domain.

### Behavioral Areas

- **with reports**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/resolve_spam_reports.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/users/resolve_spam_reports_worker.rb` -- asynchronous job processing
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

### S-1: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-2: updates statused of the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates statused of the user

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

