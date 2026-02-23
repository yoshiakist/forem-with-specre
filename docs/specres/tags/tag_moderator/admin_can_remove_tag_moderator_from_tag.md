---
id: "01KJ405WSWNE4WHSJVXZ8G81GZ"
name: "admin_can_remove_tag_moderator_from_tag"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/admin/tags/moderators_controller.rb`
- `app/services/tag_moderators/remove.rb`
- `spec/requests/admin/tags/moderators_spec.rb` (Test)
- `spec/services/tag_moderators/remove_spec.rb` (Test)

## Functional Overview

A super admin can remove a user's tag moderator role from a specific tag via `DELETE /admin/content_manager/tags/:id/moderator`. The controller looks up the user by ID and, if found, disables their tag moderator newsletter notification setting before delegating to `TagModerators::Remove`. The service strips the `tag_moderator` role from the user for that tag, invalidates the related cache entry, and — when Mailchimp integration is configured — syncs the user's status with the Mailchimp tag moderator list. The user's `trusted` role is not affected by this removal.

## Design Intent

The notification setting (`email_tag_mod_newsletter`) is disabled in the controller before calling the service so that the service's internal guard check (`email_tag_mod_newsletter?`) is already false by the time the service runs. This two-step pattern ensures the setting update failure is surfaced to the admin before any role change is attempted, and that the Mailchimp sync in the service receives a consistent state.

## Scenarios

### Successful removal

1. An authenticated super admin sends a DELETE request to `DELETE /admin/content_manager/tags/:tag_id/moderator` with the target user's ID.
2. The controller finds the user by the provided user ID.
3. The user's `email_tag_mod_newsletter` notification setting is updated to `false`.
4. `TagModerators::Remove` is called with the user and tag; it removes the `tag_moderator` role from the user for that tag.
5. The cached tag moderator list for that user is invalidated.
6. If Mailchimp is configured (both API key and tag moderator list ID are present), the user's Mailchimp subscription status is updated via `Mailchimp::Bot`.
7. A success flash message is set and the admin is redirected back to the tag's edit page.

### User not found

1. A super admin sends a DELETE request with a user ID that does not correspond to any existing user.
2. The controller sets an error flash message and immediately redirects back to the tag's edit page without invoking the remove service.

### Notification setting update fails

1. A super admin sends a valid DELETE request.
2. The controller finds the user but the `notification_setting.update` call fails validation.
3. An error flash message containing the validation errors is set and the admin is redirected to the tag's edit page without removing the role.

### Mailchimp sync skipped

1. A super admin removes a tag moderator while Mailchimp API key or tag moderator list ID is absent from `Settings::General`.
2. The role is removed and the cache is cleared, but `Mailchimp::Bot` is not invoked.

## Failures / Exceptions

- If the user ID is not found, the controller returns early with an error flash and no role change occurs.
- If updating `email_tag_mod_newsletter` fails, the controller returns early with an error flash and no role change occurs.
- The `trusted` role is intentionally preserved when a tag moderator is removed.
