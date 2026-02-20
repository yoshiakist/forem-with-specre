---
id: "01KHYAQZXMFW3CT2SJ66HTYT5A"
name: "admin_organization_memberships_controller_manages_crud"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/organization_memberships_controller.rb
- spec/requests/admin/organization_memberships_spec.rb (Test)

## Functional Overview

The Admin::OrganizationMembershipsController provides CRUD operations for organization memberships from the admin panel, supporting both HTML (redirect-based) and JS (JSON response) formats for create, update (role change), and destroy actions.

## Scenarios

### Admin creates an organization membership

1. The admin provides user_id, organization_id, and type_of_user.
2. The system validates the organization exists separately from the membership.
3. On success, the system redirects (HTML) or returns JSON with a success message (JS).
4. On failure (missing org or validation error), the system displays an error flash or returns JSON error.

### Admin updates a membership role

1. The admin changes the `type_of_user` field on an existing membership.
2. On success, the system redirects to the admin user page (HTML) or returns JSON confirmation (JS).

### Admin destroys a membership

1. The admin removes an organization membership.
2. On success, the system displays a removal success message.
3. On failure, the system displays an error message.
4. Both HTML and JS formats are supported.
