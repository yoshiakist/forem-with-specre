---
id: "01KJ9N95NCSQG1E26ZTW0TYE5W"
name: "admin_can_update_and_confirm_user_email"
status: "in-development"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `app/views/admin/users/show/emails/_verification.html.erb`
- `spec/requests/admin/users/users_update_email_spec.rb` (Test)

## Functional Overview

Admins can manage the email address and confirmation state of any user account through four distinct actions: directly overwriting the stored email address, manually marking the email as confirmed without sending a verification link, resending a Devise confirmation email to the user, and unlocking an account that Devise has locked due to too many failed sign-in attempts. Each mutating action is recorded for audit purposes via a Note on the user record, and all actions redirect back to the user's admin detail page with an appropriate flash message.

## Design Intent

Email management is kept in the admin controller rather than a dedicated service because each action maps directly to a Devise or Rails model call (`update_columns`, `confirm`, `send_confirmation_instructions`, `unlock_access!`). Using `update_columns` for email bypass validations and callbacks intentionally, since an admin override should not trigger the normal confirmation workflow. A Note is written for the two most sensitive changes (email update and manual confirm) to preserve an auditable history of who changed what and when.

## Key Members

- `update_columns(email:)` — writes the new email address directly to the database, bypassing Active Record validations and callbacks
- `Note` — audit record attached to the user with `reason`, `content`, `author_id`, and `noteable_id`
- `User#confirm` — Devise method that marks `confirmed_at` and clears the confirmation token
- `User#send_confirmation_instructions` — Devise method that generates a token and sends the confirmation email
- `User#unlock_access!` — Devise method that clears the `locked_at` timestamp and resets the failed-attempts counter

## Scenarios

### Admin updates a user's email address

1. Admin submits a new email value via the email update form on the user's admin page.
2. The system writes the new email directly to the user record, bypassing validation callbacks.
3. A Note is created recording the old email, the new email, the admin who made the change, and the reason "Update Email".
4. A success flash message is shown and the admin is redirected to the user's admin detail page.

### Admin manually confirms a user's email

1. Admin clicks "Mark as Confirmed" on the verification panel, which is only visible when the user's email is not yet confirmed.
2. The system calls Devise's `confirm` on the user, setting `confirmed_at` and clearing any pending confirmation token.
3. A Note is created recording that the email was manually confirmed and which admin performed the action.
4. A success flash message is shown and the admin is redirected back to the user's admin detail page.

### Admin resends the confirmation email

1. Admin clicks the "Send Confirmation" button on the verification panel.
2. The system calls Devise's `send_confirmation_instructions`, which generates a new confirmation token and sends the confirmation email to the user's current address.
3. A success flash message is shown and the admin is redirected back.

### Admin unlocks a locked user account

1. Admin triggers the unlock access action for a user whose account has been locked by Devise.
2. The system calls `unlock_access!` on the user, clearing the lock timestamp and resetting the failed sign-in counter.
3. A success flash message is shown and the admin is redirected to the user's admin detail page.

## Failures / Exceptions

- If `update_columns` fails (e.g., database constraint violation), an error flash is set and the admin is redirected back to the user's admin detail page; no Note is created.
- If `confirm` returns false (e.g., the user is already confirmed or a Devise validation fails), an error flash is set and the admin is redirected back; no Note is created.
- If `send_confirmation_instructions` returns false (e.g., mail delivery is not configured or the user record is invalid), an error flash is set and the admin is redirected back.
