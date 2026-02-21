---
id: "01KJ02DSNZVDY9J6F8MHMCEYZF"
name: "user_can_invite_member_to_organization"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/organizations_controller.rb`
- `app/mailers/organization_invitation_mailer.rb`
- `app/mailers/organization_membership_notification_mailer.rb`
- `app/models/organization_membership.rb`
- `spec/requests/organizations_invite_spec.rb` (Test)
- `spec/mailers/organization_invitation_mailer_spec.rb` (Test)
- `spec/mailers/organization_membership_notification_mailer_spec.rb` (Test)
- `app/views/organizations/confirm_invitation.html.erb` (Template)
- `app/views/mailers/organization_invitation_mailer/invitation_email.html.erb` (Template)
- `app/views/mailers/organization_invitation_mailer/invitation_email.text.erb` (Template)
- `app/views/mailers/organization_membership_notification_mailer/member_added_email.html.erb` (Template)
- `app/views/mailers/organization_membership_notification_mailer/member_added_email.text.erb` (Template)

## Functional Overview

An organization admin can invite an existing platform user to join their organization by submitting the user's username. For regular (non-fully-trusted) organizations, the system creates a pending `OrganizationMembership` with an auto-generated invitation token and sends the invitee an email containing a confirmation link. For fully-trusted organizations the user is added immediately as an active member and receives a notification email instead. The invitee confirms a pending invitation by visiting the tokenized URL, which renders a confirmation page; on POST the membership transitions from `pending` to `member`. Rate limits protect regular organizations from sending more than a configured number of invitations per day or accumulating too many outstanding pending invitations at once.

## Key Members

- `OrganizationMembership#type_of_user` — `"pending"` for unconfirmed invitations, `"member"` for active members, `"admin"` for organization admins
- `OrganizationMembership#invitation_token` — URL-safe random token generated on creation of a pending membership; used as the confirmation URL parameter
- `OrganizationMembership#confirm!` — transitions `type_of_user` from `"pending"` to `"member"`
- `Settings::RateLimit.organization_invitation_daily` — maximum pending invitations an organization may create in a single calendar day
- `Settings::RateLimit.organization_invitation_max_outstanding` — maximum total pending invitations allowed at any one time for a regular organization

## Scenarios

### Invite to a regular organization (pending invitation flow)

1. An admin submits a POST to `invite` with a target username (leading `@` and surrounding whitespace are stripped).
2. The system looks up the user; if not found it redirects back with an error.
3. If the user already has an active or pending membership, the system redirects back with an appropriate error.
4. The system checks the daily pending-invitation count and the total outstanding pending-invitation count against configured rate limits; if either limit is reached it redirects back with a specific error message.
5. A new `OrganizationMembership` with `type_of_user: "pending"` is created; a secure random `invitation_token` is generated automatically before save.
6. `OrganizationInvitationMailer#invitation_email` is delivered immediately. The email includes the organization name, the inviter's name (earliest non-pending admin), and a tokenized confirmation URL.
7. The admin is redirected to the organization settings page with a success notice.

### Invite to a fully-trusted organization (direct add flow)

1. An admin submits a POST to `invite` for a user not yet in the organization.
2. Rate-limit checks are skipped because the organization is fully trusted.
3. A new `OrganizationMembership` with `type_of_user: "member"` is created immediately (no token is generated).
4. `OrganizationMembershipNotificationMailer#member_added_email` is delivered immediately. The email includes the organization name, the inviter's name, and a link to the organization page.
5. The admin is redirected to the organization settings page with a success notice indicating the user was added directly.

### Invitee confirms a pending invitation (signed in)

1. The invitee clicks the confirmation link in the invitation email, which issues a GET to `confirm_invitation` with the `token` parameter.
2. The system finds the `OrganizationMembership` by token. If not found or not in `pending` state, it redirects to the root with an error.
3. If the signed-in user does not match the membership's user, the system redirects to the root with an error.
4. If the correct user is signed in on a GET request, the confirmation page is rendered showing organization details and a confirm button.
5. The invitee submits a POST to the same URL; the system calls `confirm!` which updates `type_of_user` to `"member"`.
6. The invitee is redirected to the organization settings page with a success notice.

### Invitee visits confirmation link while not signed in

1. The invitee visits the tokenized confirmation URL without being authenticated.
2. The system finds the valid pending membership and renders the confirmation page with a sign-in prompt and a link to the sign-in page (preserving the `invitation_token` parameter).

### Rate limiting blocks further invitations

1. An admin attempts to invite a user when the organization has already reached the daily invitation limit.
2. The system redirects back with an error message that includes the configured daily limit value.
3. Independently, if the total count of outstanding pending invitations reaches the max-outstanding limit (checked after the daily limit), the system redirects back with a separate error message naming that limit.

## Failures / Exceptions

- **User not found**: If no user matches the submitted username, the invite action redirects back with an error referencing the username.
- **Already a member**: If the target user already has an active membership in the organization, the action redirects back with "already a member" error.
- **Already pending**: If the target user already has a pending invitation, the action redirects back with "already has a pending invitation" error.
- **Daily rate limit exceeded**: For non-fully-trusted organizations, exceeding `Settings::RateLimit.organization_invitation_daily` pending invitations created today causes an immediate redirect with an error naming the limit count.
- **Max outstanding limit exceeded**: Exceeding `Settings::RateLimit.organization_invitation_max_outstanding` total pending invitations causes a redirect with an error naming the outstanding limit count.
- **Invalid confirmation token**: A GET or POST to `confirm_invitation` with an unrecognized token redirects to the root path with an "Invalid" error.
- **Already confirmed**: Attempting to confirm a membership that is no longer in `pending` state redirects to the root path with an "already been confirmed" error.
- **Wrong user on confirmation**: A signed-in user who is not the invitation recipient is shown an error on the confirmation page (GET) or redirected to root (POST).
- **Record validation failure**: An `ActiveRecord::RecordInvalid` exception during membership creation is rescued; the error message is set in the flash and the admin is redirected back.
