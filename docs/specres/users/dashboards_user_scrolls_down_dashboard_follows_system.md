---
id: "01KHY7Q01KJ9JFY2WBAW4M3TNF"
name: "dashboards_user_scrolls_down_dashboard_follows_system"
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
- spec/system/dashboards/user_scrolls_down_dashboard_follows_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Infinite` within the users domain.

### Behavioral Areas

- **Infinite scroll on dashboard**: /dashboard/user_followers?per_page=#{default_per_page}
- **when /dashboard/user_followers is visited**: /dashboard/user_followers?per_page=#{default_per_page}
- **when /dashboard/following_tags is visited**: Ensures correct behavior under the specified conditions
- **when /dashboard/following_users is visited**: Ensures correct behavior under the specified conditions
- **when /dashboard/following_organizations is visited**: Ensures correct behavior under the specified conditions
- **when /dashboard/following_podcasts is visited**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: /dashboard/user_followers?per_page=#{default_per_page}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /dashboard/user_followers?per_page=#{default_per_page}

### S-2: scrolls through all users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** scrolls through all users

### S-3: scrolls through all tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** scrolls through all tags

### S-4: scrolls through all users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** scrolls through all users

### S-5: scrolls through all users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** scrolls through all users

### S-6: scrolls through all podcasts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** scrolls through all podcasts

### S-7: shows working links

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows working links

