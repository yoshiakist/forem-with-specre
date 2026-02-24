---
id: "01KJ7G73NX1PNF0QQBGT8PPT41"
name: "admin_can_bulk_assign_role_to_users"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/bulk_assign_role_controller.rb`
- `app/views/admin/bulk_assign_role/index.html.erb` (Template)
- `spec/requests/admin/bulk_assign_role_spec.rb` (Test)

## Functional Overview

An admin can assign a base role to multiple users in a single operation via the bulk assign role page. The page presents a form with three fields: a role dropdown (showing base/status roles only), a comma-separated usernames textarea, and an optional note textarea. On submission, the controller splits the username list, looks up each user, and applies the selected role via `Moderator::ManageActivityAndRoles.handle_user_roles`. For every username processed, an `AuditLog` entry is created recording the role, username, and outcome status (`role_applied_successfully`, `user_already_has_the_role`, or `user_not_found`). If no role is selected, an `ArgumentError` is raised immediately and no users are modified. On success, the admin is redirected back to the bulk assign page with a flash success message; on any other error, a flash danger message is shown instead.

## Design Intent

The bulk operation creates an `AuditLog` entry for every username in the list, even when a user is not found or already holds the role, providing a complete audit trail of what was attempted and what outcome each username produced.

## Key Members

- `role` — the selected base role string; must be non-blank or an `ArgumentError` is raised
- `usernames` — comma-separated string of usernames, lowercased and split on whitespace-tolerant commas
- `note_for_current_role` — optional note recorded against each role assignment; defaults to an i18n string if omitted
- `user_action_status` — per-username outcome: `role_applied_successfully`, `user_already_has_the_role`, or `user_not_found`

## Scenarios

### Admin successfully assigns a role to multiple users

1. Admin navigates to the bulk assign role page.
2. Admin selects a base role from the dropdown, enters a comma-separated list of usernames, and optionally provides a note.
3. Admin submits the form.
4. The system applies the role to each valid user.
5. An `AuditLog` entry with category `admin.bulk_assign_role.add_role` and status `role_applied_successfully` is created for each user.
6. Admin is redirected back to the page with a success flash message.

### Admin enters usernames with extra whitespace

1. Admin submits the form with usernames that have extra spaces around commas (e.g., `user1,  user2`).
2. The system strips the extra whitespace when splitting the list.
3. Each user receives the role as if the input were clean.

### Admin submits without selecting a role

1. Admin submits the form without selecting a role from the dropdown.
2. The system raises an `ArgumentError` immediately, before processing any usernames.
3. No roles are assigned and no `AuditLog` entries are created.
4. Admin is redirected back to the page with a danger flash message.

### Admin enters a username that does not exist

1. Admin submits the form with a mix of valid and invalid usernames.
2. The system applies the role to all valid users.
3. For the unrecognised username, no role assignment is attempted, but an `AuditLog` entry with status `user_not_found` is still created.
4. Admin is redirected back to the page with a success flash message.

### Admin assigns a role a user already holds

1. Admin submits the form for a user who already has the specified role.
2. The system calls the role management handler regardless, but records the outcome as `user_already_has_the_role` in the `AuditLog`.

### Admin omits the note field

1. Admin submits the form without entering a note.
2. The system substitutes a default i18n note string that includes the role name.
3. The default note is stored against each user's role assignment.

## Failures / Exceptions

- If `role` is blank, an `ArgumentError` is raised and the controller rescues it, setting a danger flash and redirecting without modifying any users.
- Any `StandardError` raised during the per-username loop (e.g., from the role management service) is caught, sets a danger flash with the error message, and halts further processing.
