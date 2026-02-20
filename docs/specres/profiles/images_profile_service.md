---
id: "01KHY7Q0MAD2GXWE7B4NMHZKKT"
name: "images_profile_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/profile_field_groups_controller.rb
- app/controllers/admin/profile_fields_controller.rb
- app/controllers/api/v0/profile_images_controller.rb
- app/controllers/api/v1/profile_images_controller.rb
- app/controllers/concerns/api/profile_images_controller.rb
- app/controllers/profile_field_groups_controller.rb
- app/controllers/profile_pins_controller.rb
- app/controllers/profile_preview_cards_controller.rb
- app/controllers/profiles_controller.rb
- app/decorators/profile_decorator.rb
- app/helpers/profile_helper.rb
- app/models/profile.rb
- app/models/profile_field.rb
- app/models/profile_field_group.rb
- app/models/profile_pin.rb
- spec/services/images/profile_spec.rb

## Functional Overview

This specification defines the expected behavior of `Images::Profile` within the profiles domain.

### Behavioral Areas

- **.for**: Ensures correct behavior under the specified conditions
- **when mixed in**: Ensures correct behavior under the specified conditions
- **.get**: Ensures correct behavior under the specified conditions
- **when user has no profile_image**: returns user profile_image_url

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_pins_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_preview_cards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profiles_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/profile_decorator.rb` -- presentation logic and view-model enrichment
- **View helper**: `app/helpers/profile_helper.rb` -- shared view utility methods
- **Model layer**: `app/models/profile.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- be a Module

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: creates a method

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a method

### S-3: forward delegate the method to Images::Profile.call

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** forward delegate the method to Images::Profile.call

### S-4: returns user profile_image_url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user profile_image_url

### S-5: returns backup image prefixed with Cloudinary

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns backup image prefixed with Cloudinary

