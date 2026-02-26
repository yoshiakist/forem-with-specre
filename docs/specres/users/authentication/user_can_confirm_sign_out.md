---
id: "01KJBGZF9PRSHNVF807K57AY46"
name: "user_can_confirm_sign_out"
status: "draft"
---

## Related Files

- `app/controllers/users_controller.rb`
- `app/controllers/sessions_controller.rb`
- `app/controllers/concerns/session_current_user.rb`
- `app/views/users/signout_confirm.html.erb` (Template)
- `app/views/devise/sessions/new.html.erb` (Template)
- `spec/requests/sessions_spec.rb` (Test)

## Functional Overview

When a signed-in user navigates to the sign-out confirmation page, the application renders a dedicated confirmation view that prompts the user to explicitly consent to signing out. The page presents a single confirmation button. When the user clicks the button, a client-side script clears the browser's localStorage and marks the session as signing out in sessionStorage before submitting the Devise DELETE session form. The `SessionsController#destroy` action then clears the user's `current_sign_in_at` and `current_sign_in_ip` columns, deletes the `forem_user_signed_in` cookie, and delegates to Devise to destroy the server-side session and redirect to the sign-in page. Throughout the application, the `SessionCurrentUser` concern resolves the current user's ID from the Warden session key.

## Design Intent

localStorage is cleared on the client before the sign-out request is submitted to avoid stale client-side data persisting after the session ends. A sessionStorage flag (`isSigningOut`) is set so that other client-side code can distinguish a deliberate sign-out from a normal page unload. The sign-out itself is delegated to Devise via a DELETE request to `destroy_user_session_path`, keeping authentication logic out of the application controller. Clearing `current_sign_in_at` and `current_sign_in_ip` on the server ensures the tracked fields do not remain set after session end. If a user is redirected back to the sign-out confirmation page after signing back in, the application redirects them to the root path instead.

## Scenarios

### User visits the sign-out confirmation page

1. A signed-in user navigates to the sign-out confirmation page (e.g., by clicking a "Sign out" link elsewhere in the application).
2. The `signout_confirm` controller action renders the confirmation view with a page title drawn from the community name locale string.
3. The page displays a heading and a single confirmation button labeled with the locale string for "Yes".

### User confirms sign-out

1. The user clicks the confirmation button on the sign-out confirmation page.
2. The browser's localStorage is cleared entirely.
3. A `isSigningOut` flag is written to sessionStorage to signal an intentional sign-out.
4. The hidden Devise sign-out form (targeting `destroy_user_session_path` with the DELETE method) is programmatically submitted.
5. `SessionsController#destroy` clears `current_sign_in_at` and `current_sign_in_ip` on the user record, and deletes the `forem_user_signed_in` cookie for the current host.
6. Devise destroys the server-side session and redirects the user to the sign-in page (`app/views/devise/sessions/new.html.erb`), completing the sign-out flow.

### User does not confirm sign-out

1. The user navigates away from the confirmation page without clicking the button.
2. No localStorage is cleared, no sign-out form is submitted, and the user remains signed in.

### Unauthenticated DELETE request to sign-out endpoint

1. A request is made to `DELETE /users/sign_out` when no user is signed in.
2. The `SessionsController#destroy` guard (`if user_signed_in?`) skips the cleanup steps.
3. Devise handles the request and redirects without raising an error.
