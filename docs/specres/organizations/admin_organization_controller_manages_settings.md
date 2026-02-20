---
id: "01KHYAQZFNE6166KPD56KDPFRQ"
name: "admin_organization_controller_manages_settings"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/organizations_controller.rb
- spec/requests/admin/organizations_spec.rb (Test)
- spec/requests/admin/organizations_baseline_score_spec.rb (Test)
- spec/requests/admin/organizations_fully_trusted_spec.rb (Test)

## Functional Overview

The Admin::OrganizationsController provides the admin interface for managing organizations, including paginated listing with search, viewing details, modifying credit balances, toggling fully-trusted status, updating baseline scores, and scheduling deletion — all with audit trail via Note records.

## Scenarios

### Admin lists organizations with optional search

1. The admin views a paginated list of organizations (max 50 per page) ordered by creation date descending.
2. If a search parameter is provided, the system filters organizations by name using case-insensitive matching.

### Admin views organization details

1. The admin views a single organization by ID.

### Admin updates organization credits

1. The admin specifies a credit amount and action (add or remove).
2. The system calls `Credit.add_to` or `Credit.remove_from` on the organization.
3. The system creates a Note record as an audit trail with the admin's note content.

### Admin toggles fully-trusted status

1. The admin sets fully_trusted to true or false.
2. If the status changed, the system creates a Note record documenting the change.
3. The system displays a flash message reflecting the new status.

### Admin updates baseline score

1. The admin provides a new baseline score integer.
2. The system updates the organization and creates a Note recording the old-to-new score change.

### Admin schedules organization deletion

1. The system enqueues `Organizations::DeleteWorker` with `deleted_by_org_admin=false`.
2. If an error occurs, the system displays an error flash and redirects.
