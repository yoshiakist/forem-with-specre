---
id: "01KJVS5357MREJ2TCGFTFFESGH"
name: "admin_can_view_and_update_spaces"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/policies/space_policy.rb`
- `app/controllers/admin/spaces_controller.rb`
- `app/models/space.rb`
- `spec/policies/space_policy_spec.rb` (Test)
- `spec/models/space_spec.rb` (Test)

## Functional Overview

Administrators and super-administrators can view the Space settings page and update the singleton Space configuration. The Space model is not an ActiveRecord object; it is an ActiveModel-backed value object that acts as a thin facade over feature flags. The only setting currently exposed is `limit_post_creation_to_admins`, which controls who may create posts. On update, the controller enforces authorization, saves the Space (which toggles the underlying feature flag), logs the action to the audit trail, and busts content-change caches so that downstream views reflect the new setting immediately.

## Design Intent

Space is intentionally implemented as a non-persisted ActiveModel object rather than a database-backed record. This keeps the initial authorization use-case simple and avoids schema migrations while still providing a Rails-idiomatic form interface. The singleton pattern (`to_param` always returns `"default"`) ensures a conventional RESTful resource URL without requiring a lookup. The cache-busting after_action ensures that any cached homepage fragments depending on space settings are invalidated immediately after an admin changes them.

## Key Members

- `limit_post_creation_to_admins: Boolean` — when true, only admins may create posts; maps directly to the `:limit_post_creation_to_admins` feature flag.

## Scenarios

### Admin views the Space settings page

1. An admin or super-admin navigates to the admin spaces index path.
2. The controller authorizes the request against `SpacePolicy#index?`, which delegates to `user_any_admin?`.
3. A new, default-initialized `Space` instance is prepared for the view's settings form.
4. The settings page renders with the current feature flag state pre-populated in the form.

### Admin updates Space settings

1. An admin submits the Space settings form with the desired `limit_post_creation_to_admins` value.
2. The controller builds a new `Space` instance from the permitted params and authorizes it via `SpacePolicy#update?`.
3. `Space#save` is called: it enables or disables the `:limit_post_creation_to_admins` feature flag accordingly, then enqueues `Spaces::BustCachesForSpaceChangeWorker`.
4. The audit logger records the action with the acting user and submitted params.
5. Content-change caches are busted via the `bust_content_change_caches` after_action.
6. The admin is redirected to the spaces index (HTML) or receives a JSON success message (JSON).

### Non-admin is denied access

1. A user without admin or super-admin role attempts to access the spaces index or submit an update.
2. `SpacePolicy#index?` or `SpacePolicy#update?` returns false because `user_any_admin?` is false.
3. The request is rejected by Pundit's authorization layer.

### Unauthenticated user is denied access

1. An unauthenticated request reaches the spaces index or update action.
2. The policy requires an authenticated user; the request is rejected before reaching any Space logic.
