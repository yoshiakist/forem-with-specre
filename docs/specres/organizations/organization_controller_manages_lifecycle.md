---
id: "01KHYAPESAA0V3WKK075E59EPH"
name: "organization_controller_manages_lifecycle"
status: "draft"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/organizations_controller.rb
- spec/requests/organizations_update_spec.rb (Test)
- spec/requests/organizations_invite_spec.rb (Test)
- spec/requests/organizations_members_spec.rb (Test)

## Functional Overview

The OrganizationsController handles public-facing organization lifecycle operations: creating new organizations with admin membership, updating organization profiles with image validation, scheduling asynchronous deletion, generating new secrets, viewing members, inviting users (with rate limiting for non-trusted orgs), and confirming invitation tokens.

## Scenarios

### User creates a new organization

1. The system enforces rate limiting on organization creation.
2. The system validates the uploaded profile image for file type and filename length.
3. The system strips HTML tags from all string parameters.
4. On successful save, the system creates an admin OrganizationMembership for the current user and redirects to organization settings.
5. On validation failure, the system re-renders the edit form.

### User updates an existing organization

1. The system authorizes the current user as an org admin.
2. The system validates the profile image and updates the organization with `profile_updated_at`.
3. On success, the system touches `organization_info_updated_at` on all organization users and redirects.
4. On failure, the system re-renders the edit form with membership context.

### User destroys an organization

1. The system authorizes the destroy action via OrganizationPolicy.
2. The system enqueues `Organizations::DeleteWorker` with `deleted_by_org_admin=true`.
3. If authorization fails, the system displays an error flash and redirects.

### User generates a new organization secret

1. The system authorizes the current user, generates a new random secret, saves it, and redirects.

### Visitor views organization members

1. The system looks up the organization by slug; returns 404 if not found.
2. The system returns active (non-pending) users as JSON or HTML.

### User invites another user to the organization

1. The system authorizes the current user for update access.
2. The system looks up the target user by username; shows error if not found.
3. The system checks for existing membership (active or pending) and rejects duplicates.
4. For non-fully-trusted organizations, the system enforces daily and total outstanding invitation rate limits.
5. For fully-trusted organizations, the system creates an active "member" membership and sends a member-added email.
6. For regular organizations, the system creates a "pending" membership and sends an invitation email.

### User confirms an invitation

1. The system looks up the membership by invitation token; redirects with error if invalid or already confirmed.
2. If the user is not signed in, the system renders the confirmation page.
3. If the signed-in user does not match the invited user, the system rejects with an error.
4. On POST, the system confirms the membership and redirects to organization settings.
5. On GET, the system renders the confirmation page.
