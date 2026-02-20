---
id: "01KHY7PZWF8M275D484FSNZMZS"
name: "registrations_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/registrations_controller.rb
- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/queries/admin/gdpr_delete_requests_query.rb
- spec/requests/registrations_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Registrations"` within the users domain.

### Behavioral Areas

- **Registrations**: Ensures correct behavior under the specified conditions
- **Log In**: Ensures correct behavior under the specified conditions
- **when not logged in**: creates user when email in allow list
- **when email login is enabled in /admin/customization/config**: shows the sign in page with email option
- **when email login is disabled in /admin/customization/config**: shows the sign in page with email option
- **when logged in**: creates user when email in allow list
- **when subforem redirect conditions are met**: redirects to main feed
- **when subforem_id is set but subforem record is not found**: redirects to the subforem enter path with the provided state

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/registrations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/admin/gdpr_delete_requests_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: shows the sign in page with single sign on options

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the sign in page with single sign on options

### S-2: only shows the single sign on options if they are present

- **Given** they are present
- **When** the action is triggered
- **Then** only shows the single sign on options

### S-3: shows the sign in text for password based authentication

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the sign in text for password based authentication

### S-4: does not show the sign in text for password based authentication

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show the sign in text for password based authentication

### S-5: redirects to main feed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to main feed

### S-6: redirects to the subforem enter path with the provided state

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the subforem enter path with the provided state

### S-7: falls through and renders the normal sign up page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls through and renders the normal sign up page

### S-8: shows the sign in page with email option

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the sign in page with email option

### S-9: shows the sign in text for password based authentication

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the sign in text for password based authentication

### S-10: persists uploaded image

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** persists uploaded image

### S-11: creates a user with a random profile image if none was uploaded

- **Given** none was uploaded
- **When** the action is triggered
- **Then** creates a user with a random profile image

### S-12: does not show email sign up option

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show email sign up option

