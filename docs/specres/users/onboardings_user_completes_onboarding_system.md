---
id: "01KHY7Q01X77NM0PT8DK32MN8W"
name: "onboardings_user_completes_onboarding_system"
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
- spec/system/onboardings/user_completes_onboarding_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Completing` within the users domain.

### Behavioral Areas

- **Completing Onboarding**: does not render the onboarding task card on the feed
- **when the user hasn**: Ensures correct behavior under the specified conditions
- **when the user has seen onboarding**: does not render the onboarding task card on the feed
- **when site limits article creation to admins**: Ensures correct behavior under the specified conditions
- **when user is admin**: Ensures correct behavior under the specified conditions
- **when user is not an admin**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: does not render the onboarding task card on the feed

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render the onboarding task card on the feed

### S-2: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-3: logs in and renders the feed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs in and renders the feed

### S-4: renders the feed and onboarding task card

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the feed and onboarding task card

### S-5: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-6: shows a call to action for creating a post and can dismiss the onboarding task c...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows a call to action for creating a post and can dismiss the onboarding task card

### S-7: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-8: renders the feed and onboarding task card

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the feed and onboarding task card

### S-9: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-10: does not render a Create a Post call to action in the onboarding task card

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render a Create a Post call to action in the onboarding task card

### S-11: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

