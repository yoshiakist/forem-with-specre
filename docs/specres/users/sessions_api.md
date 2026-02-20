---
id: "01KHY7PZWJ9PKWTK4KA3E55ZB9"
name: "sessions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/sessions_controller.rb
- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/queries/admin/gdpr_delete_requests_query.rb
- spec/requests/sessions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Sessions"` within the users domain.

### Behavioral Areas

- **Sessions**: Ensures correct behavior under the specified conditions
- **POST /users/sign_in**: Ensures correct behavior under the specified conditions
- **DELETE /users/sign_out**: signs the user out, clears tracked fields, and deletes the forem_user_signed_in cookie
- **when user is signed in**: signs the user in and updates tracked fields
- **when user is not signed in**: signs the user in and updates tracked fields

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/sessions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/admin/gdpr_delete_requests_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: signs the user in and updates tracked fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** signs the user in and updates tracked fields

### S-2: fails to sign in with invalid credentials

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fails to sign in with invalid credentials

### S-3: redirects to root path if stored location is /signout_confirm

- **Given** stored location is /signout_confirm
- **When** the action is triggered
- **Then** redirects to root path

### S-4: signs the user out, clears tracked fields, and deletes the forem_user_signed_in ...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** signs the user out, clears tracked fields, and deletes the forem_user_signed_in cookie

### S-5: does not raise an error and simply redirects

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not raise an error and simply redirects

