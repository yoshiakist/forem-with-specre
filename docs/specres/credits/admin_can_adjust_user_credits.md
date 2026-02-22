---
id: "01KJ2SFWXPPE61BA7KNFY8CSSG"
name: "admin_can_adjust_user_credits"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/credits/manage.rb`
- `app/models/credit.rb`
- `app/views/admin/users/modals/_adjust_credits_modal.html.erb` (Template)
- `app/views/admin/users/show/overview/_credits.html.erb` (Template)
- `spec/services/credits/manage_spec.rb` (Test)
- `spec/requests/admin/users_manage_spec.rb` (Test)

## Functional Overview

An admin can adjust the credit balance of a user or an organization through the admin user management UI. The admin submits a form specifying an action (add or remove) and an amount; the `Credits::Manage` service dispatches to `Credit.add_to` or `Credit.remove_from` accordingly, then updates cached credit counts on the owner. The same service handles both user-level and organization-level credit adjustments in a single call, skipping each operation when its corresponding parameter is absent.

## Design Intent

All four adjustment operations (add/remove for user, add/remove for organization) are dispatched in sequence within a single `call` invocation. Each private method guards itself with an early return when its parameter is missing, so callers only need to pass the relevant subset of parameters without branching logic outside the service. The `Credit.remove_from` implementation is capped at the owner's actual balance — it will not produce a negative credit count.

## Key Members

- `user_params[:add_credits]` — integer string; number of credits to add to the user
- `user_params[:remove_credits]` — integer string; number of unspent credits to remove from the user
- `org_params[:add_org_credits]` — integer string; number of credits to add to the organization
- `org_params[:remove_org_credits]` — integer string; number of credits to remove from the organization
- `org_params[:organization_id]` — ID used to look up the target organization

## Scenarios

### Admin adds credits to a user

1. Admin navigates to the user's admin overview page, which shows the user's current unspent credit balance.
2. Admin clicks the "Adjust Balance" button, which opens the adjust-credits modal pre-filled with the user's name and current balance.
3. Admin selects "Add", enters an amount between 1 and 9999, writes a note, and submits.
4. `Credits::Manage` is called with `add_credits` set to the entered amount; `Credit.add_to` bulk-inserts that many unspent credit records for the user.
5. The user's `credits_count`, `spent_credits_count`, and `unspent_credits_count` cache columns are updated immediately.

### Admin removes credits from a user

1. Admin opens the adjust-credits modal for the target user and selects "Remove" with a specified amount.
2. `Credits::Manage` is called with `remove_credits` set to the entered amount; `Credit.remove_from` deletes that many unspent credit records, limited to the user's actual balance.
3. Cache columns on the user are updated to reflect the new balance.

### Admin adds credits to an organization

1. Admin submits a request with `add_org_credits` and `organization_id` parameters for the target user's page.
2. `Credits::Manage` resolves the organization via `organization_id`, then calls `Credit.add_to` with the organization and the specified amount.
3. The organization's cached credit counts are updated.

### Admin removes credits from an organization

1. Admin submits a request with `remove_org_credits` and `organization_id` parameters.
2. `Credits::Manage` resolves the organization and calls `Credit.remove_from`, removing up to the specified number of unspent credits without going below zero.
3. The organization's cached credit counts are updated.

## Failures / Exceptions

- If `add_credits` or `remove_credits` is absent from the parameters, the corresponding operation is silently skipped.
- If `add_org_credits` or `remove_org_credits` is absent, the corresponding organization operation is silently skipped.
- `Credit.add_to` short-circuits and inserts nothing if the amount is not positive.
- `Credit.remove_from` will not create a negative balance; it removes at most the number of unspent credits the owner currently holds.
