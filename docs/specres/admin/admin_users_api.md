---
id: "01KHY7Q146KBEEXMZ1BBBZSC16"
name: "admin_users_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/users_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/member_manager/users"` within the admin domain.

### Behavioral Areas

- **/admin/member_manager/users**: Ensures correct behavior under the specified conditions
- **GET /admin/member_manager/users**: Ensures correct behavior under the specified conditions
- **when searching**: displays a message when there are no related vomit reactions for a user
- **when filtering by role**: displays a message when there are no related vomit reactions for a user
- **GET /admin/member_manager/users/:id**: Ensures correct behavior under the specified conditions
- **POST /admin/member_manager/users/:id/banish**: displays a label if an unpublished post was republished
- **POST /admin/member_manager/users/:id/send_email**: displays a label if an unpublished post was republished
- **when interacting via a browser**: displays a message when there are no related vomit reactions for a user


## Scenarios

### S-1: renders to appropriate page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders to appropriate page

### S-2: finds the proper user by GitHub username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds the proper user by GitHub username

### S-3: filters and shows the proper user(s)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters and shows the proper user(s)

### S-4: renders to appropriate page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders to appropriate page

### S-5: redirects from /username/moderate

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects from /username/moderate

### S-6: shows banish button for new users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows banish button for new users

### S-7: does not show banish button for non-admins

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show banish button for non-admins

### S-8: displays a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a user

### S-9: displays a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a user

### S-10: displays a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a user

### S-11: displays a message when there are no related vomit reactions for a user

- **Given** the system is in a standard operational state
- **When** there are no related vomit reactions for a user
- **Then** displays a message

### S-12: displays a list of recent related vomit reactions for a user if any exist

- **Given** any exist
- **When** the action is triggered
- **Then** displays a list of recent related vomit reactions for a user

