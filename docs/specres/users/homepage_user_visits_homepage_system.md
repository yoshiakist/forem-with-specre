---
id: "01KHY7Q01R76ENYS8CW8W48Y06"
name: "homepage_user_visits_homepage_system"
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
- spec/system/homepage/user_visits_homepage_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User visits a homepage**: hides link when display_to is set to logged in users only
- **when user hasn**: shows expected number of links when signed out
- **link tags**: shows the tags block
- **navigation_links**: shows the correct navigation_links
- **when logged in user**: shows expected number of links when signed out
- **when rendering broadcasts**: shows expected number of links when signed out
- **when user follows tags**: shows the tags block
- **navigation_links**: shows the correct navigation_links

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: shows the sign-in block

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the sign-in block

### S-2: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-3: shows the tags block

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the tags block

### S-4: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-5: contains the qualified community name in the search link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the qualified community name in the search link

### S-6: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-7: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-8: shows expected number of links when signed out

- **Given** the system is in a standard operational state
- **When** signed out
- **Then** shows expected number of links

### S-9: shows the Other section when other nav links exist

- **Given** the system is in a standard operational state
- **When** other nav links exist
- **Then** shows the Other section

### S-10: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-11: hides link when display_to is set to logged in users only

- **Given** the system is in a standard operational state
- **When** display_to is set to logged in users only
- **Then** hides link

### S-12: shows links in their correct section and order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows links in their correct section and order

