---
id: "01KHY7Q15RKTPXQCP5604C22TZ"
name: "admin_config_admin_updates_smtp_settings_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/system/admin/config/admin_updates_smtp_settings_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin updates SMTP Settings**: shows the SMTP Form
- **when Sendgrid is not enabled and SMTP is not enabled**: shows the SMTP Form
- **when Sendgrid is enabled and SMTP is not enabled**: shows the SMTP Form
- **when Sendgrid is not enabled and SMTP is enabled**: shows the SMTP Form
- **when Sendgrid is enabled and SMTP is enabled**: shows the SMTP Form


## Scenarios

### S-1: does not show the 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show the 

### S-2: shows the SMTP Form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the SMTP Form

### S-3: shows the checkbox to allow one to toggle ones own server

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the checkbox to allow one to toggle ones own server

### S-4: shows a description

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows a description

### S-5: does not show an SMTP Form

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show an SMTP Form

### S-6: does not show the 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show the 

### S-7: shows the SMTP Form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the SMTP Form

### S-8: shows the 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the 

### S-9: shows an SMTP Form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows an SMTP Form

