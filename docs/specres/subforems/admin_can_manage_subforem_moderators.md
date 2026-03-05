---
id: "01KHYH2RE3WEHN4RVYZWBNXCHA"
name: "admin_can_manage_subforem_moderators"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/subforem_moderators/moderators_controller.rb
- app/services/subforem_moderators/add.rb
- app/services/subforem_moderators/add_trusted_role.rb
- app/services/subforem_moderators/remove.rb
- app/views/mailers/notify_mailer/subforem_moderator_confirmation_email.html.erb (Template)
- app/views/mailers/notify_mailer/subforem_moderator_confirmation_email.text.erb (Template)
- spec/services/subforem_moderators/add_spec.rb (Test)
- spec/services/subforem_moderators/remove_spec.rb (Test)

## Functional Overview

Administrators, super moderators, and existing subforem moderators can add or remove moderators for a specific subforem. Adding a moderator assigns the `:subforem_moderator` role, grants the `:trusted` role if needed, enables community moderator newsletter notifications, syncs with Mailchimp, and sends a confirmation email. Removing a moderator revokes the role, updates notification preferences, and clears the moderator list cache.

## Design Intent

Moderator management is split into small service objects (`SubforemModerators::Add`, `AddTrustedRole`, `Remove`) so that each operation is independently testable and can be called from different entry points (admin UI, future API). The `AddTrustedRole` service is separated because the trusted role grant has its own side effects (email, Mailchimp sync) that should not be duplicated.

## Scenarios

### Admin adds a subforem moderator

1. Admin navigates to the subforem show page and submits a username
2. System looks up the user by username
3. System calls `SubforemModerators::Add` which enables community mod newsletter notifications on the user
4. System assigns the `:subforem_moderator` role scoped to the subforem
5. System grants the `:trusted` role via `AddTrustedRole` if the user is not already trusted and not suspended or spam
6. System sends a confirmation email via `NotifyMailer`
7. System syncs the moderator with the Mailchimp community moderators list (if configured)
8. System clears the subforem's moderator list cache
9. Admin is redirected back to the subforem show page

### Admin removes a subforem moderator

1. Admin clicks the remove button next to a moderator on the subforem show page
2. System calls `SubforemModerators::Remove` which revokes the `:subforem_moderator` role
3. System updates notification settings if the user had community mod newsletter enabled
4. System syncs the removal with the Mailchimp community moderators list (if configured)
5. System clears the subforem's moderator list cache
6. Admin is redirected back to the subforem show page

### Authorization restricts access

1. Only users with admin, super_moderator, or subforem_moderator roles can access moderator management
2. Users without these roles receive a forbidden response

## Failures / Exceptions

- If the notification settings update fails during add, the service returns a failure result with errors and does not assign the moderator role
- If the user lookup by username finds no match, the controller handles the missing user gracefully
