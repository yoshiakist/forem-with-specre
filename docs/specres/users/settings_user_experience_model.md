---
id: "01KHY7PZTHZQCM214V4BZFYAM8"
name: "settings_user_experience_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/user_experiences_controller.rb
- app/lib/constants/settings/user_experience.rb
- app/models/settings/user_experience.rb
- app/controllers/admin/settings/authentications_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/lib/constants/settings/authentication.rb
- app/models/settings/authentication.rb
- app/services/settings/authentication/upsert.rb
- spec/models/settings/user_experience_spec.rb

## Functional Overview

This specification defines the expected behavior of `Settings::UserExperience` within the users domain.

### Behavioral Areas

- **validating hex string format**: allows 3 character hex strings
- **validating color contrast**: allows high enough color contrast
- **cover image settings**: has a default cover_image_height of 420
- **cover_image_aesthetic_instructions**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- `app/lib/constants/settings/user_experience.rb`
- **Model layer**: `app/models/settings/user_experience.rb` -- data persistence, validations, and associations
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- `app/lib/constants/settings/authentication.rb`
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/settings/authentication/upsert.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: allows 3 character hex strings

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows 3 character hex strings

### S-2: allows 6 character hex strings

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows 6 character hex strings

### S-3: rejects strings without leading #

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects strings without leading #

### S-4: rejects invalid character

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid character

### S-5: allows high enough color contrast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows high enough color contrast

### S-6: rejects too low color contrast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects too low color contrast

### S-7: has a default cover_image_height of 420

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has a default cover_image_height of 420

### S-8: has a default cover_image_fit of 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has a default cover_image_fit of 

### S-9: allows setting cover_image_height

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows setting cover_image_height

### S-10: allows setting cover_image_fit to 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows setting cover_image_fit to 

### S-11: rejects invalid cover_image_fit values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid cover_image_fit values

### S-12: has an empty default value

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has an empty default value

