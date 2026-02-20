---
id: "01KHY7Q02573ZHS0G2NSB8497V"
name: "organization_user_views_an_organization_system"
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
- spec/system/organization/user_views_an_organization_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Organization` within the users domain.

### Behavioral Areas

- **Organization index**: /#{organization.slug}
- **when user does not follow organization**: /#{organization.slug}
- **when 2 articles**: shows articles
- **when more articles**: shows articles
- **when more than 8 articles**: shows articles
- **when user follows an organization**: /#{organization.slug}
- **when there are multiple members in the organization within a limit**: /#{organization.slug}
- **when there are more than 50 members in the organization**: /#{organization.slug}

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: /#{organization.slug}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{organization.slug}

### S-2: shows the header

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the header

### S-3: shows articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles

### S-4: shows the sidebar

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the sidebar

### S-5: shows the right amount of articles in sidebar

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the right amount of articles in sidebar

### S-6: shows the proper title tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the proper title tag

### S-7: visits ok

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** visits ok

### S-8: /#{organization.slug}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{organization.slug}

### S-9: /#{organization.slug}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{organization.slug}

### S-10: tells the user the correct amount of posts published

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** tells the user the correct amount of posts published

### S-11: shows the correct button

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the correct button

### S-12: /#{organization.slug}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{organization.slug}

