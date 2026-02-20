---
id: "01KHYAN2Z8BX8EQWF0T0B3J5XB"
name: "organization_membership_mailer_notifies_member_added"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/organization_membership_notification_mailer.rb
- app/views/mailers/organization_membership_notification_mailer/member_added_email.html.erb
- app/views/mailers/organization_membership_notification_mailer/member_added_email.text.erb
- spec/mailers/organization_membership_notification_mailer_spec.rb (Test)

## Functional Overview

The OrganizationMembershipNotificationMailer sends a notification email when a user is directly added to an organization (as opposed to being invited). It identifies the person who added them from non-pending memberships excluding the new member, and renders both HTML and plain-text templates with the organization context and a link to the organization profile.

## Scenarios

### Mailer sends member-added notification email

1. The mailer receives a `membership_id` parameter and looks up the OrganizationMembership.
2. The mailer extracts the user, organization, and identifies the inviter as the earliest non-pending member excluding the new member.
3. The mailer sends an email to the added user's address with a subject including the organization name and community name.
4. The HTML template includes the inviter's name (if available), an explanation of organizations, and a styled link to the organization profile.
5. The plain-text template includes the same content with a raw URL to the organization.
