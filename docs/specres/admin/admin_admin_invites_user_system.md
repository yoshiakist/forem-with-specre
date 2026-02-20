---
id: "01KHY7Q14ZMZQYMBGSXK56TPNE"
name: "admin_admin_invites_user_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/system/admin/admin_invites_user_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin invites user**: Ensures correct behavior under the specified conditions
- **when SMTP is not configured**: contains a link to configure SMTP settings
- **when SMTP is configured**: contains a link to configure SMTP settings


## Scenarios

### S-1: shows a header

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows a header

### S-2: shows a banner

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows a banner

### S-3: contains a link to the documentation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains a link to the documentation

### S-4: contains a link to configure SMTP settings

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains a link to configure SMTP settings

### S-5: does not contain any for fields

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not contain any for fields

### S-6: does not contain any submit buttons

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not contain any submit buttons

### S-7: shows the input field

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the input field

### S-8: shows the submit button

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the submit button

