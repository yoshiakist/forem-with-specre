---
id: "01KHY7Q03K4D1WTRHYGXPYW90H"
name: "videos_user_visits_videos_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/controllers/admin/settings/authentications_controller.rb
- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/admin/user_queries_controller.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- spec/system/videos/user_visits_videos_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User visits the videos page**: /videos
- **when user hasn**: Ensures correct behavior under the specified conditions
- **meta tags**: contains the expected title tags

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: /videos

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /videos

### S-2: contains the qualified community name in og:site_name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the qualified community name in og:site_name

### S-3: contains the expected title tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the expected title tags

