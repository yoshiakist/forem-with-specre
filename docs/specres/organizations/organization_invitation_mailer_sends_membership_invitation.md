---
id: "01KHYAN2EY716NJQJ4P7XGBTDG"
name: "organization_invitation_mailer_sends_membership_invitation"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/organization_invitation_mailer.rb
- app/views/mailers/organization_invitation_mailer/invitation_email.html.erb
- app/views/mailers/organization_invitation_mailer/invitation_email.text.erb
- spec/mailers/organization_invitation_mailer_spec.rb (Test)

## Functional Overview

The OrganizationInvitationMailer sends an invitation email to a user who has been invited to join an organization. It identifies the inviter from the earliest non-pending membership, generates a token-based confirmation URL, and renders both HTML and plain-text email templates with organization context and a confirmation link.

## Scenarios

### Mailer sends invitation email with confirmation link

1. The mailer receives a `membership_id` parameter and looks up the OrganizationMembership.
2. The mailer extracts the user, organization, and identifies the inviter as the earliest non-pending member.
3. The mailer generates a confirmation URL using the membership's invitation token and the app domain.
4. The mailer sends an email to the invited user's address with a subject including the organization name and community name.
5. The HTML template includes the inviter's name (if available), an explanation of organizations, and a styled confirmation button.
6. The plain-text template includes the same content with a raw confirmation URL.
