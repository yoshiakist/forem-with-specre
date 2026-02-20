---
id: "01KHY7PZWC0D45JZVN2BDP311D"
name: "auth_passes_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/queries/admin/gdpr_delete_requests_query.rb
- spec/requests/auth_passes_spec.rb

## Functional Overview

This specification defines the expected behavior of `"AuthPassController"` within the users domain.

### Behavioral Areas

- **AuthPassController**: Ensures correct behavior under the specified conditions
- **POST /auth_pass/token_login**: Ensures correct behavior under the specified conditions
- **with a valid token and allowed origin**: authenticates the user, sets the remember_user_token cookie, and returns success: true
- **with an invalid token**: authenticates the user, sets the remember_user_token cookie, and returns success: true
- **with an expired token**: authenticates the user, sets the remember_user_token cookie, and returns success: true
- **with an unauthorized origin**: returns success: false with 

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/admin/gdpr_delete_requests_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: authenticates the user, sets the remember_user_token cookie, and returns success...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** authenticates the user, sets the remember_user_token cookie, and returns success: true

### S-2: returns success: false with 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success: false with 

### S-3: returns success: false with 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success: false with 

### S-4: does not set CORS headers and returns status ok

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set CORS headers and returns status ok

