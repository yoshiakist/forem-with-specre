---
id: "01KHY7Q115HXFA4F0ESJMHC6XJ"
name: "admin_emails_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/emails_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/emails"` within the admin domain.

### Behavioral Areas

- **/admin/emails**: Ensures correct behavior under the specified conditions
- **GET /admin/emails**: Ensures correct behavior under the specified conditions
- **GET /admin/emails/new**: Ensures correct behavior under the specified conditions
- **POST /admin/emails**: Ensures correct behavior under the specified conditions
- **with valid parameters**: renders the new template with a form
- **with invalid parameters**: renders the new template with a form
- **GET /admin/emails/:id**: Ensures correct behavior under the specified conditions
- **PATCH /admin/emails/:id**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: renders the index template and displays emails

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the index template and displays emails

### S-2: renders the new template with a form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the new template with a form

### S-3: creates a new email and redirects to its page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new email and redirects to its page

### S-4: does not create a new email and re-renders the new template

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new email and re-renders the new template

### S-5: renders the show template for the email and replaces merge tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the show template for the email and replaces merge tags

### S-6: updates the email and redirects to its page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the email and redirects to its page

### S-7: does not update the email and re-renders the edit template

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not update the email and re-renders the edit template

### S-8: calls deliver_to_test_emails

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls deliver_to_test_emails

