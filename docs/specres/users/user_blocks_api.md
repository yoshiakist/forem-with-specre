---
id: "01KHY7PZXAPBD4M5D96JJAVRE1"
name: "user_blocks_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/user_blocks_controller.rb
- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/queries/admin/gdpr_delete_requests_query.rb
- spec/requests/user_blocks_spec.rb

## Functional Overview

This specification defines the expected behavior of `"UserBlock"` within the users domain.

### Behavioral Areas

- **UserBlock**: raises ActiveRecord::RecordNotFound error if UserBlock not found
- **GET /user_blocks/:blocked_id or #show**: Ensures correct behavior under the specified conditions
- **POST /user_blocks or #create**: Ensures correct behavior under the specified conditions
- **DELETE /user_blocks/:blocked_id or #delete**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/user_blocks_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/admin/gdpr_delete_requests_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: rejects when not-logged-in

- **Given** the system is in a standard operational state
- **When** not-logged-in
- **Then** rejects

### S-2: returns 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 

### S-3: returns 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 

### S-4: renders 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders 

### S-5: creates the correct user_block

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates the correct user_block

### S-6: returns a JSON response with blocked

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a JSON response with blocked

### S-7: renders 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders 

### S-8: renders 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders 

### S-9: raises ActiveRecord::RecordNotFound error if UserBlock not found

- **Given** UserBlock not found
- **When** the action is triggered
- **Then** raises ActiveRecord::RecordNotFound error

### S-10: removes the correct user_block

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the correct user_block

