---
id: "01KHY7Q11NAX3Y73F40HXC7FXY"
name: "admin_invitations_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/invitations_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/member_manager/invitations"` within the admin domain.

### Behavioral Areas

- **/admin/member_manager/invitations**: Ensures correct behavior under the specified conditions
- **GET /admin/member_manager/invitations**: Ensures correct behavior under the specified conditions
- **GET /admin/member_manager/invitations/new**: Ensures correct behavior under the specified conditions
- **POST /admin/member_manager/invitations**: Ensures correct behavior under the specified conditions
- **POST /admin/member_manager/invitations/:id/resend**: Ensures correct behavior under the specified conditions
- **DELETE /admin/member_manager/invitations**: deletes the invitation


## Scenarios

### S-1: renders to appropriate page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders to appropriate page

### S-2: renders to appropriate page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders to appropriate page

### S-3: creates new invitation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates new invitation

### S-4: enqueues an invitation email to be sent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues an invitation email to be sent

### S-5: enqueues an invitation email to be sent with custom subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues an invitation email to be sent with custom subject

### S-6: does not create an invitation if a user with that email exists

- **Given** a user with that email exists
- **When** the action is triggered
- **Then** does not create an invitation

### S-7: enqueues an invitation email to be resent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues an invitation email to be resent

### S-8: deletes the invitation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the invitation

