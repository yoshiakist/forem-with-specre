---
id: "01KHYASY8DESB0ZXJFQZTWXPC8"
name: "admin_organizations_helper_validates_deletion"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/helpers/admin/organizations_helper.rb
- spec/helpers/admin/organizations_helper_spec.rb (Test)

## Functional Overview

The Admin::OrganizationsHelper provides a deletion modal error message generator that checks the current admin's role and the organization's credit balance to build contextual warning messages for the deletion confirmation dialog.

## Scenarios

### Helper builds deletion warning based on role and credits

1. If the current user is not a super admin, the helper includes a role notice warning.
2. If the organization has credits, the helper appends a credits notice warning.
3. If both conditions apply, the warnings are concatenated and stripped.
4. If neither condition applies, the helper returns nil (no warning needed).
