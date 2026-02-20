---
id: "01KHY7PZVMKJ3ZDBN44397FT5K"
name: "users_setting_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/models/users/notification_setting.rb
- app/models/users/setting.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users_controller.rb
- app/helpers/admin/users_helper.rb
- app/helpers/users_helper.rb
- spec/models/users/setting_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::Setting` within the users domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **validating color fields**: is valid if the field is a correct hex color with leading #
- **config_theme**: Ensures correct behavior under the specified conditions
- **content_preferences_input**: Ensures correct behavior under the specified conditions
- **config_font**: Ensures correct behavior under the specified conditions
- **config_navbar**: Ensures correct behavior under the specified conditions
- **config_homepage_feed**: Ensures correct behavior under the specified conditions
- **when validating feed_url**: is valid with no feed_url

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/users/notification_setting.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/users/setting.rb` -- data persistence, validations, and associations
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate length of inbox guidelines.is at most 250.allow nil
- validate numericality of experience level.is in 1..10
- validate inclusion of disallow subforem reassignment.in array [true, false]
- define enum for inbox type.with values private: 0, open: 1.with suffix inbox
- define enum for config font.with values default: 0, comic sans: 1, monospace: 2, open dyslexic: 3, sans serif: 4, serif: 5.with suffix font
- define enum for config navbar.with values default: 0, static: 1.with suffix navbar
- define enum for config theme.with values light theme: 0, dark theme: 2
- define enum for config homepage feed.with values default: 0, latest: 1, top week: 2, top month: 3, top year: 4, top infinity: 5.with suffix feed

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is valid if the field is a correct hex color with leading #

- **Given** the field is a correct hex color with leading #
- **When** the action is triggered
- **Then** is valid

### S-3: is valid if the field is a correct hex color without leading #

- **Given** the field is a correct hex color without leading #
- **When** the action is triggered
- **Then** is valid

### S-4: is valid if the field is a 3-digit hex color

- **Given** the field is a 3-digit hex color
- **When** the action is triggered
- **Then** is valid

### S-5: is valid if the brand color is nil

- **Given** the brand color is nil
- **When** the action is triggered
- **Then** is valid

### S-6: is invalid if the field is too long

- **Given** the field is too long
- **When** the action is triggered
- **Then** is invalid

### S-7: is invalid if the field contains non hex characters

- **Given** the field contains non hex characters
- **When** the action is triggered
- **Then** is invalid

### S-8: accepts valid theme

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid theme

### S-9: does not accept invalid theme

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not accept invalid theme

### S-10: updates content_preferences_updated_at if changed

- **Given** changed
- **When** the action is triggered
- **Then** updates content_preferences_updated_at

### S-11: does not update content_preferences_updated_at if empty

- **Given** empty
- **When** the action is triggered
- **Then** does not update content_preferences_updated_at

### S-12: does not update if not changed

- **Given** not changed
- **When** the action is triggered
- **Then** does not update

### S-13: accepts valid font

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid font

