---
id: "01KHY7Q1559K03TFTRH34Z7SNR"
name: "admin_admin_manages_pages_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/system/admin/admin_manages_pages_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin manages pages**: does not show any of the links in the pages table
- **when there are default pages**: shows an override defaults section with a warning
- **when the defaults are overridden**: shows an override defaults section with a warning
- **when there is a landing page**: does not show any of the links in the pages table
- **when a Forem is private**: Ensures correct behavior under the specified conditions
- **when a Forem is public**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: loads the view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** loads the view

### S-2: shows an override defaults section with a warning

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows an override defaults section with a warning

### S-3: shows the code of conduct link in the overrides section

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the code of conduct link in the overrides section

### S-4: shows the privacy policy link in the overrides section

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the privacy policy link in the overrides section

### S-5: shows the terms of use link in the overrides section

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the terms of use link in the overrides section

### S-6: does not show any of the links in the pages table

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show any of the links in the pages table

### S-7: has client-side validation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has client-side validation

### S-8: allows a page to be deleted

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows a page to be deleted

### S-9: shows the notice that the defaults have been overridden

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the notice that the defaults have been overridden

### S-10: shows the overridden pages in the pages table

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the overridden pages in the pages table

### S-11: allows a landing page to be updated

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows a landing page to be updated

### S-12: allows an Admin to click through to the current landing page via the modal

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to click through to the current landing page via the modal

