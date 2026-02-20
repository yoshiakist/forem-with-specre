---
id: "01KHY7Q0MDP32PSS9PNZS135P7"
name: "images_safe_remote_profile_image_url_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/images/safe_remote_profile_image_url.rb
- app/controllers/api/v0/profile_images_controller.rb
- app/controllers/api/v1/profile_images_controller.rb
- app/controllers/concerns/api/profile_images_controller.rb
- app/services/images/profile.rb
- app/services/images/profile_image_generator.rb
- spec/services/images/safe_remote_profile_image_url_spec.rb

## Functional Overview

This specification defines the expected behavior of `Images::SafeRemoteProfileImageUrl` within the profiles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/images/safe_remote_profile_image_url.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/images/profile.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/images/profile_image_generator.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns the url if passed for proper URLs

- **Given** passed for proper URLs
- **When** the action is triggered
- **Then** returns the url

### S-2: returns fallback image if passed nil

- **Given** passed nil
- **When** the action is triggered
- **Then** returns fallback image

### S-3: returns fallback image if passed blank

- **Given** passed blank
- **When** the action is triggered
- **Then** returns fallback image

### S-4: returns fallback image if passed non-URL

- **Given** passed non-URL
- **When** the action is triggered
- **Then** returns fallback image

### S-5: returns a secure HTTPS image link if pass a regular HTTP link

- **Given** pass a regular HTTP link
- **When** the action is triggered
- **Then** returns a secure HTTPS image link

