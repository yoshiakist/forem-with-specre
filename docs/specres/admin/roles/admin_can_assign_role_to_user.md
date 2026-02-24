---
id: "01KJ7G7M4JRVA0J8VWAVJ7Y5ME"
name: "admin_can_assign_role_to_user"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/users_controller.rb` (Tagged: 01KJ75DN218QHHZ575VBJ95H29, 01KJ759KKVVQ8YQZP1B78QC3Q6)
- `app/services/moderator/manage_activity_and_roles.rb`
- `app/models/role.rb`
- `app/models/user_role.rb`
- `app/lib/constants/role.rb`
- `app/views/admin/users/modals/_add_role_modal.html.erb` (Template)
- `app/views/admin/users/show/overview/_roles.html.erb` (Template)
- `app/views/mailers/notify_mailer/trusted_role_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/trusted_role_email.text.erb` (Template)
- `app/views/mailers/notify_mailer/base_subscriber_role_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/base_subscriber_role_text.html.erb` (Template)
- `spec/services/moderator/manage_activity_and_roles_spec.rb` (Test)
- `spec/models/role_spec.rb` (Test)
- `spec/models/user_role_spec.rb` (Test)

## Functional Overview

An admin navigates to a user's detail page and sees the user's current roles listed as removable pills; if no roles exist, a placeholder message is shown. Clicking "Add Role" opens a modal form presenting a grouped dropdown of base roles (Warned, Comment Suspended, Limited, Suspended, Spam, Base Subscriber, Good standing, Trusted) and special roles (Admin, Tech Admin, Super Admin, and various Resource Admin scopes). The admin selects a role and enters a mandatory note, then submits. The `user_status` action delegates to `Moderator::ManageActivityAndRoles.handle_user_roles`, which applies role-specific logic: elevated roles (Admin, Super Admin, Super Moderator, Tech Admin) require the acting admin to be a super_admin and remove all negative roles before granting the new role; the Trusted role also removes negative roles and triggers a trusted-role email; negative roles (Suspended, Spam, Limited, Warned, Comment Suspended) strip mod privileges before adding the restriction; Good standing removes all negative and mod roles; Base Subscriber adds the role and sends a subscriber email; Resource Admin roles require super_admin privilege and grant `single_resource_admin` scoped to the specified resource type. A Note is always created recording the acting admin and the reason, and all of the user's published articles and comments have their scores recalculated after the change.

## Design Intent

Role transitions are centralized in `Moderator::ManageActivityAndRoles` so that each role type's invariants (privilege removal, cache invalidation, email notifications, score recalculation) are enforced consistently regardless of where in the admin UI the action originates. Elevated admin roles also invalidate the `Rack::Attack` admin API allow-list cache so that security controls take effect immediately without a server restart.

## Key Members

- `user_status` — The human-readable role label submitted from the modal form (e.g. `"Trusted"`, `"Suspended"`, `"Resource Admin: Article"`). Drives the case dispatch inside `handle_user_status`.
- `note_for_current_role` — Mandatory free-text note recorded on the `Note` object alongside the change.
- `Constants::Role::BASE_ROLES` — Labels available in the base-roles group of the dropdown.
- `Constants::Role::SPECIAL_ROLES` — Labels available in the special-roles group; all require super_admin to apply.

## Scenarios

### Admin assigns an elevated role (Admin, Super Admin, Super Moderator, Tech Admin)

1. The acting admin must hold the super_admin role; if not, the system raises an error and the role is not changed.
2. The system removes any negative roles (limited, suspended, spam, warned, comment_suspended) currently held by the target user.
3. The new elevated role is added to the user; for Admin, Super Admin, and Super Moderator the Trusted role is also granted automatically.
4. For roles that appear in the Rack::Attack admin bypass list, the admin API cache key is cleared so the updated access list takes effect immediately.
5. For Tech Admin, `single_resource_admin` scoped to `DataUpdateScript` is also added.
6. A Note is created, and article and comment scores are recalculated.

### Admin assigns the Trusted role

1. Any negative roles held by the user are removed.
2. `TagModerators::AddTrustedRole` is called, which grants the trusted role and sends the trusted-role email to the user.
3. A Note is created, and scores are recalculated.

### Admin assigns a negative/restrictive role (Warned, Suspended, Spam, Limited, Comment Suspended)

1. The chosen restrictive role is added to the user.
2. For Warned, any existing suspended or spam roles are also removed.
3. The user's mod privileges are stripped: the trusted and tag_moderator roles are removed and Mailchimp list memberships are updated.
4. For Spam, spam reports referencing the user are resolved, flag reactions are confirmed, the user's profile cache is busted, and their notifications are asynchronously removed.
5. A Note is created, and scores are recalculated.

### Admin restores a user to Good standing

1. All negative roles (limited, suspended, spam, warned, comment_suspended) are removed.
2. All mod roles (trusted, tag_moderator) are removed and Mailchimp memberships are updated.
3. A Note is created, and scores are recalculated.

### Admin assigns the Base Subscriber role

1. The `base_subscriber` role is added to the user.
2. The user record and profile are touched to bust caches.
3. The `base_subscriber_role_email` is delivered immediately to the user.
4. A Note is created, and scores are recalculated.

## Failures / Exceptions

- Attempting to assign any elevated role (Admin, Super Admin, Super Moderator, Tech Admin, or any Resource Admin) when the acting admin is not a super_admin raises a `StandardError` with a localized message; the controller rescues this and sets a flash danger message.
- Any other `StandardError` raised during role processing is caught by the `user_status` action and returned as a flash danger message (HTML) or a JSON error response with HTTP 422.
