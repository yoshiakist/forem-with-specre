---
id: "01KHY7PZW1AYNG87XJPFCW6EAM"
name: "admin_user_marks_user_as_spam_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/queries/admin/gdpr_delete_requests_query.rb
- spec/requests/admin_user_marks_user_as_spam_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Spam` within the users domain.

### Behavioral Areas

- **Spam Toggling for User**: marks user as spam
- **PUT /users/:id/spam**: Ensures correct behavior under the specified conditions
- **when user exists**: marks user as spam
- **when user does not exist**: marks user as spam
- **when unauthorized**: Ensures correct behavior under the specified conditions
- **DELETE /users/:id/spam**: Ensures correct behavior under the specified conditions
- **when user exists and is marked as spam**: marks user as spam
- **when user does not exist**: marks user as spam

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/admin/gdpr_delete_requests_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: marks user as spam

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks user as spam

### S-2: returns a not found status

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a not found status

### S-3: prevents non-admins from marking a user as spam

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents non-admins from marking a user as spam

### S-4: removes user from spam

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes user from spam

### S-5: returns a not found status

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a not found status

### S-6: prevents non-admins from removing a user from spam

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents non-admins from removing a user from spam

