---
id: "01KHZ6G82HEH34EH9QFG6JJ8XC"
name: "admin_can_manage_user_from_profile_page"
status: "draft"
---

## Related Files

- `app/views/admin/users/show/_profile.html.erb`
- `app/views/admin/users/show/profile/_actions.html.erb`
- `app/views/admin/users/show/profile/_status.html.erb`
- `app/views/admin/users/show/profile/actions/_change_max_score.html.erb`
- `app/views/admin/users/show/profile/actions/_change_reputation.html.erb`
- `app/views/admin/users/show/profile/actions/_delete.html.erb`
- `app/views/admin/users/show/profile/actions/_edit_profile.html.erb`
- `app/views/admin/users/show/profile/actions/_export.html.erb`
- `app/views/admin/users/show/profile/actions/_merge.html.erb`
- `app/views/admin/users/show/profile/actions/_social_accounts.html.erb`
- `app/views/admin/users/show/profile/actions/_update_email.html.erb`
- `spec/requests/user/user_profile_spec.rb` (Test)
- `spec/routing/profile_admin_routes_spec.rb` (Test)
- `spec/requests/admin/users/users_update_email_spec.rb` (Test)

## Functional Overview

The admin user profile page displays a summary of a user's identity — avatar, name, username, registration date, email, and linked social accounts — alongside a status badge reflecting their current moderation state (e.g., Spam, Suspended, Warned, Trusted). From a dropdown actions menu, an admin can perform a wide range of management operations on that user: editing core profile fields, updating their email address, exporting their data, merging the account into another, removing social account identities, adjusting the reputation modifier, setting a maximum score cap, unlocking a locked account, unpublishing all posts, banishing the user for spam, or permanently deleting the account. Each destructive or form-based action is surfaced in a modal that loads its content from hidden partial templates rendered alongside the main profile.

## Scenarios

### Viewing user identity and status

1. Admin navigates to the admin user show page.
2. The profile section renders the user's avatar, display name, username, numeric ID, and registration date.
3. If the account is locked, a danger notice appears with an "Unlock" link above the profile card.
4. A status badge next to the user's name reflects their current role: Spam, Suspended, Warned, Comment Suspended, Limited, Trusted, or Good Standing.
5. If the user has a positive `max_score`, an additional badge showing the cap value appears alongside the status badge.

### Editing core profile fields

1. Admin opens the options dropdown and selects "Edit profile".
2. A modal opens with a form pre-populated with the user's current name, username, summary, location, and website URL.
3. Admin modifies any field and submits, sending a PATCH request to `update_profile_admin_user_path`.

### Updating the user's email address

1. Admin opens the options dropdown and selects "Update email".
2. A modal opens displaying the user's current email and an input for a new email address.
3. Admin enters the new address and submits, sending a PATCH request to `update_email_admin_user_path`.

### Adjusting reputation modifier or max score

1. Admin opens the options dropdown and selects "Change reputation" or "Change max score".
2. A modal opens showing the current value and fields for a new numeric value and a mandatory change note.
3. Admin fills in the new value and note, then submits a PATCH request to `reputation_modifier_admin_user_path` or `max_score_admin_user_path` respectively.

### Merging, removing social accounts, exporting data, and deleting

1. Admin opens the options dropdown and selects one of the destructive or data actions.
2. For account merge, a modal prompts for the target user ID and requires browser-level confirmation before submitting a POST to `merge_admin_user_path`.
3. For social account removal, a modal lists each linked identity with a delete button; confirming removes that identity via a DELETE request to `remove_identity_admin_user_path`.
4. For data export, a modal offers two buttons: send export to the admin email or to the user's email, both posting to `export_data_admin_user_path` with a `send_to_admin` flag.
5. For permanent deletion, the option is only visible to super admins; submitting requires browser-level confirmation and posts to `full_delete_admin_user_path`. Non-super-admins see a danger notice instead of the form.

## Failures / Exceptions

- The "Delete user" form is replaced with a danger notice for any admin who is not a super admin, preventing accidental or unauthorized permanent deletion.
- The "Unpublish all posts" action is only shown in the dropdown when the user has at least one article (`articles_count > 0`).
- The "Remove social accounts" option is only shown in the dropdown when the user has at least one linked identity.
