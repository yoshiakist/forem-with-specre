---
id: "01KHY7Q0M794J5PT2FE6113H9X"
name: "images_profile_image_generator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/images/profile_image_generator.rb
- app/controllers/api/v0/profile_images_controller.rb
- app/controllers/api/v1/profile_images_controller.rb
- app/controllers/concerns/api/profile_images_controller.rb
- app/services/images/profile.rb
- app/services/images/safe_remote_profile_image_url.rb
- spec/services/images/profile_image_generator_spec.rb

## Functional Overview

This specification defines the expected behavior of `Images::ProfileImageGenerator` within the profiles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/images/profile_image_generator.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/images/profile.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/images/safe_remote_profile_image_url.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns an image file

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an image file

