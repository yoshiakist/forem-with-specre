---
id: "01KHYCGB56TKXQNTVJHKN58M32"
name: "admin_assigns_tag_moderators"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/tags/moderators_controller.rb
- spec/requests/admin/tags/moderators_spec.rb (Test)

## Functional Overview

`Admin::Tags::ModeratorsController` allows administrators to assign and remove tag moderator roles for users. Adding a moderator grants the user the `tag_moderator` role (scoped to a specific tag) and the `trusted` role, and enables their tag moderator newsletter setting. Removing a moderator revokes the role and disables the newsletter setting. All actions are audit-logged.

## Scenarios

### Admin adds a tag moderator

1. The admin submits a username to add as a moderator for a specific tag.
2. The system looks up the user by username; if not found, an error message is displayed and the admin is redirected back.
3. On success, `TagModerators::Add` grants the user the `tag_moderator` role scoped to the tag, grants the `trusted` role, and enables `email_tag_mod_newsletter` on the user's notification settings.
4. A success flash message confirms the addition.
5. If `TagModerators::Add` returns a failure result, an error message with details is displayed.

### Admin removes a tag moderator

1. The admin submits a user ID to remove from a specific tag's moderators.
2. The system looks up the user by ID; if not found, an error message is displayed.
3. The user's `email_tag_mod_newsletter` notification setting is set to false.
4. `TagModerators::Remove` revokes the `tag_moderator` role for that tag (the `trusted` role is preserved).
5. A success flash message confirms the removal.

### All moderator actions are audited

1. Both create and destroy actions log the operation via `Audit::Logger` with the moderator action type, the acting admin user, and the request parameters.
