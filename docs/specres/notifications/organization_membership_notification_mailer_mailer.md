---
id: "01KHY7Q05CTCXDK5JMBRK83MKE"
name: "organization_membership_notification_mailer_mailer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/organization_membership_notification_mailer.rb
- spec/mailers/organization_membership_notification_mailer_spec.rb

## Functional Overview

This specification defines the expected behavior of `OrganizationMembershipNotificationMailer` within the notifications domain.

### Behavioral Areas

- **member_added_email**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: renders the headers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the headers

### S-2: includes organization information

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes organization information

### S-3: includes organization URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes organization URL

### S-4: includes inviter information when available

- **Given** the system is in a standard operational state
- **When** available
- **Then** includes inviter information

### S-5: includes explanation of organizations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes explanation of organizations

### S-6: does not include confirmation link

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include confirmation link

