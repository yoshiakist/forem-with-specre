---
id: "01KJ9G05S72CY68YM2GMN7W01Q"
name: "admin_resends_user_invitation"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/invitations_controller.rb`
- `app/views/admin/users/index/_invitation_actions_dropdown.html.erb`
- `spec/requests/admin/invitations_spec.rb` (Test)

## Functional Overview

When an admin wants to re-invite a user who has not yet completed registration, they trigger the resend action from the invitation actions dropdown on the admin users index page. The system looks up the unregistered user by ID and calls the invite method on that user. If the invite succeeds, a success flash message is set with the user's email; if it fails, a danger flash message is set with the error details. Either way, the admin is redirected back to the admin invitations listing page.

## Scenarios

### Admin successfully resends an invitation

1. Admin navigates to the admin users index page and opens the dropdown menu for a pending (unregistered) user.
2. Admin clicks the "Resend" button, which submits a POST request to the resend invitation endpoint for that user.
3. The system finds the user by ID, confirming they are not yet registered.
4. The system calls the invite method on the user, which enqueues a Devise invitation email containing "invitation_instructions" for delivery.
5. A success flash message is displayed with the invited user's email address, and the admin is redirected to the invitations listing page.

### Admin attempts to resend but the invite action fails

1. Admin submits a resend request for an unregistered user.
2. The system finds the user but the invite method returns a failure (e.g., validation errors on the user record).
3. A danger flash message is displayed containing the error details from the user record.
4. The admin is redirected to the invitations listing page without an email being sent.

## Failures / Exceptions

- If the user is not found or is already registered, the lookup (`User.where(registered: false).find`) raises a record not found error.
- If the invite action fails, the user's validation errors are rendered as a sentence in a danger flash message rather than a success message.
