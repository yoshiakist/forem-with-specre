---
id: "01KHYAQZFNE6166KPD56KDPFRQ"
name: "admin_can_manage_organizations"
status: "draft"
---

## Related Files

- `app/controllers/admin/organizations_controller.rb`
- `spec/requests/admin/organizations_spec.rb` (Test)

## Functional Overview

The `Admin::OrganizationsController` provides the unified admin interface for organization lifecycle management. It exposes five actions — `index`, `show`, `update_org_credits`, `update_fully_trusted`, `update_baseline_score`, and `destroy` — all protected by the admin layout and admin authentication. The controller uses a shared `add_note` method to create audit trail entries (`Note` records) against the organization, ensuring all privileged changes are recorded with the admin's identity and a descriptive content string. Pagination is capped at 50 records per page via `PER_PAGE_MAX`. Credit action dispatching uses a frozen hash (`CREDIT_ACTIONS`) that maps symbolic action names to `Credit` class method names, raising `KeyError` on unrecognized values to prevent silent failures.

This card describes the controller as an integration surface. Individual behaviors are documented in detail by dedicated specre cards:

- Listing and viewing: `admin_can_view_organizations` (`01KJ02MNP5AREF4M1SM48V0ED6`)
- Credits, trust, and baseline score: `admin_can_adjust_organization_credits_and_trust` (`01KJ02MSM04C2X6Q5EEC8T55ZC`)
- Deletion: `user_can_delete_organization` (`01KJ029Q7RK57YNH11SH1V2BBB`)

## Key Members

- `PER_PAGE_MAX = 50` — maximum number of organizations displayed per page on the index
- `CREDIT_ACTIONS` — frozen indifferent-access hash mapping `add` to `:add_to` and `remove` to `:remove_from`; used by `update_org_credits` to dispatch to `Credit.add_to` or `Credit.remove_from`
- `Admin::OrganizationsController#add_note` — private method that creates a `Note` record with the current admin as author, the organization as noteable, reason `"misc_note"`, and content from the request params

## Scenarios

### Admin navigates the organization management interface

1. An authenticated admin visits the organizations index at `/admin/content_manager/organizations`.
2. The system returns up to 50 organizations per page, ordered by creation date (newest first) unless a search term is provided.
3. The admin clicks into a specific organization to see its detail page with profile, activity, credits, and management actions.
4. From the detail page, the admin can adjust credits (with an audit note), toggle fully-trusted status, update the baseline score, or schedule deletion.
5. All modification actions create `Note` audit records and redirect back to the organization detail page with a flash notice.

### Unrecognized credit action is submitted

1. An admin submits a credit adjustment with a `credit_action` value that is neither `"add"` nor `"remove"`.
2. `CREDIT_ACTIONS.fetch(params[:credit_action])` raises `KeyError` because no default is provided.
3. The request fails with an unhandled exception rather than silently ignoring the invalid action.
