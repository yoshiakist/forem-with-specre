---
id: "01KHY7Q0KKHMR583EYZ7FQW2SE"
name: "profile_model"
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
- spec/models/profile_spec.rb

## Functional Overview

This specification defines the expected behavior of `Profile` within the profiles domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **conditionally validating summary**: is not valid if the summary is too long and the user is not grandfathered
- **validating text areas**: is valid if the text is short enough
- **validating text fields**: is valid if the text is short enough
- **validating website_url**: enqueues a profile spam check when website_url changes
- **when accessing profile fields**: counts line ending as a single character when summary is multi line
- **cache busting**: enqueues a profile details cache bust when summary changes
- **profile spam checks**: defines accessors for active profile fields

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

- validate uniqueness of user id

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is valid if users previously had long summaries and are grandfathered

- **Given** users previously had long summaries and are grandfathered
- **When** the action is triggered
- **Then** is valid

### S-3: is not valid if the summary is too long and the user is not grandfathered

- **Given** the summary is too long and the user is not grandfathered
- **When** the action is triggered
- **Then** is not valid

### S-4: is valid if the summary is less than the limit

- **Given** the summary is less than the limit
- **When** the action is triggered
- **Then** is valid

### S-5: counts line ending as a single character when summary is multi line

- **Given** the system is in a standard operational state
- **When** summary is multi line
- **Then** counts line ending as a single character

### S-6: is valid if the text is short enough

- **Given** the text is short enough
- **When** the action is triggered
- **Then** is valid

### S-7: is invalid if the text is too long

- **Given** the text is too long
- **When** the action is triggered
- **Then** is invalid

### S-8: is valid if text contains new-lines within 200 characters

- **Given** text contains new-lines within 200 characters
- **When** the action is triggered
- **Then** is valid

### S-9: is valid if the text is short enough

- **Given** the text is short enough
- **When** the action is triggered
- **Then** is valid

### S-10: is invalid if the text is too long

- **Given** the text is too long
- **When** the action is triggered
- **Then** is invalid

### S-11: is valid if blank

- **Given** blank
- **When** the action is triggered
- **Then** is valid

### S-12: is valid with a complete url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid with a complete url

### S-13: is invalid with an incomplete url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid with an incomplete url

