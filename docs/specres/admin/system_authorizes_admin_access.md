---
id: "01KJ9GW0HAGR8XG1KN5GETDK8Q"
name: "system_authorizes_admin_access"
status: "draft"
---

## Related Files

- `app/controllers/admin/application_controller.rb`
- `app/policies/admin_policy.rb`
- `app/policies/internal_policy.rb`
- `spec/policies/admin_policy_spec.rb` (Test)
- `spec/policies/internal_policy_spec.rb` (Test)
- `spec/requests/shared_examples/internal_policy_dependant_request.rb` (Test)

## Functional Overview

The admin panel enforces authorization via a base controller that gates every action through a `before_action` that delegates to `InternalPolicy`. `AdminPolicy` provides two access levels: `show?` permits only super_admin users to proceed, while `minimal?` permits any admin user. After each action, Pundit's `after_action :verify_authorized` ensures no action was inadvertently left unguarded. A contextual help URL is also assigned per controller, pointing admins to relevant documentation.

## Design Intent

Authorization is Pundit-based, using `InternalPolicy` as the primary gatekeeping mechanism for all admin controllers. `AdminPolicy` is kept minimal and composable, separating super_admin-only access (`show?`) from broader admin access (`minimal?`), so individual feature controllers can choose the appropriate permission check. The `verify_authorized` after-action hook acts as a safety net, catching any controller that forgets to call `authorize`.

## Key Members

- `authorize_admin` — `before_action` that calls Pundit's `authorize` with `InternalPolicy` on the inferred resource class for the current controller.
- `authorization_resource` — derives the resource class from the controller name by stripping the `Admin::` namespace prefix and `Controller` suffix, then singularizing and constantizing.
- `AdminPolicy#show?` — returns true only for super_admin users.
- `AdminPolicy#minimal?` — returns true for any admin user.
- `HELP_URLS` — frozen hash mapping controller names to their corresponding admin documentation URLs.

## Scenarios

### Super admin accesses an admin panel page

1. A super_admin user navigates to any page under the admin namespace.
2. The base controller's `before_action` fires `authorize_admin`, which resolves the resource class from the controller name and calls `authorize` via `InternalPolicy`.
3. `InternalPolicy` delegates to the appropriate policy; if `AdminPolicy#show?` is consulted, it returns true for super_admin.
4. The action proceeds and a contextual help URL is assigned.
5. After the action, `verify_authorized` confirms authorization was called.

### Regular admin (non-super) accesses a page that requires only minimal? permission

1. A user with admin (but not super_admin) privileges requests an admin page where the policy check resolves to `minimal?`.
2. `authorize_admin` is invoked; `AdminPolicy#minimal?` returns true because the user is any_admin.
3. The action proceeds normally.

### Non-admin user attempts to access the admin panel

1. A regular user (no admin role) attempts to access any page in the admin namespace.
2. `authorize_admin` calls `authorize` via `InternalPolicy`; both `show?` and `minimal?` return false.
3. Pundit raises `Pundit::NotAuthorizedError` and the request is rejected.

### Super_admin-only page rejects a regular admin

1. A user with admin (but not super_admin) privileges requests a page that requires `show?`.
2. `AdminPolicy#show?` returns false because the user is not a super_admin.
3. Authorization fails and the user is denied access.

## Failures / Exceptions

- Any user without admin privileges who attempts to access the admin namespace receives a `Pundit::NotAuthorizedError`.
- A regular admin accessing a super_admin-only resource is also denied with `Pundit::NotAuthorizedError`.
- If a subclass controller action omits an `authorize` call, `verify_authorized` raises `Pundit::AuthorizationNotPerformedError` after the action completes.
