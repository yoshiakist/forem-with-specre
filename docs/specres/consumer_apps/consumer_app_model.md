---
id: "01KHY7Q1K82NPWADJKPHWX8CGS"
name: "consumer_app_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/consumer_apps_controller.rb
- app/models/consumer_app.rb
- app/policies/consumer_app_policy.rb
- spec/models/consumer_app_spec.rb

## Functional Overview

This specification defines the expected behavior of `ConsumerApp` within the consumer_apps domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **operational?**: Ensures correct behavior under the specified conditions
- **with non-Forem apps**: returns true/false based on the ENV variable for the Forem apps
- **with Forem apps**: returns true/false based on the ENV variable for the Forem apps
- **after an update**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/consumer_apps_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/consumer_app.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/consumer_app_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- have many devices.dependent destroy
- validate presence of app bundle
- validate uniqueness of app bundle.scoped to platform

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: returns false if not active in DB or if credentials are unavailable

- **Given** not active in DB or if credentials are unavailable
- **When** the action is triggered
- **Then** returns false

### S-3: returns true if both active and credentials are available for Android

- **Given** both active and credentials are available for Android
- **When** the action is triggered
- **Then** returns true

### S-4: returns true if both active and credentials are available for iOS

- **Given** both active and credentials are available for iOS
- **When** the action is triggered
- **Then** returns true

### S-5: returns true/false based on the ENV variable for the Forem apps

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true/false based on the ENV variable for the Forem apps

### S-6: recreates the Rpush app for Android

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** recreates the Rpush app for Android

### S-7: recreates the Rpush app for iOS

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** recreates the Rpush app for iOS

