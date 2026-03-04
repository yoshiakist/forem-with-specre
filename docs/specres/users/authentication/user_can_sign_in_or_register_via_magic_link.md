---
id: "01KJVJ01ZBWZ49FSMYNE8GM1CQ"
name: "user_can_sign_in_or_register_via_magic_link"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/magic_links_controller.rb`
- `app/views/magic_links/new.html.erb` (Template)
- `app/views/magic_links/create.html.erb` (Template)
- `spec/requests/magic_links_spec.rb` (Test)

## Functional Overview

A visitor or existing user can sign in or create an account by submitting their email address on the magic link request page. If the email matches an existing user, the system sends that user a magic link email. If no user exists and the instance is not invite-only, the system auto-registers a new user with a generated username, name, and profile image, skipping the normal confirmation email, then sends the magic link. The user is taken to a confirmation screen and given 20 minutes to enter the code (the token embedded in the link). When the user visits the magic link URL, the system looks up the token, confirms the user's email if not yet confirmed, signs them in, and redirects to the home page. Expired or unknown tokens are rejected with an alert.

## Design Intent

New users are registered silently with a random Devise-compatible password because magic link auth requires no password. Confirmation is deferred — the account is created unconfirmed and the `confirmed_at` timestamp is set only at the moment the link is clicked. This avoids the standard Devise confirmation email while still preserving the confirmed state after first sign-in. The 20-minute window balances usability and security.

## Key Members

- `sign_in_token` — random token stored on the user and embedded in the magic link URL
- `sign_in_token_sent_at` — timestamp used to enforce the 20-minute expiry window
- `confirmed_at` — set at link click time if not already present; not overwritten for already-confirmed users
- `onboarding_subforem_id` — assigned to new users based on the request host at registration time

## Scenarios

### Visitor requests a magic link for an existing email

1. Visitor navigates to the magic link request page (`GET /magic_links/new`).
2. Visitor enters their email and submits the form.
3. System finds a matching user and calls `send_magic_link!` to dispatch the token email.
4. System renders the confirmation view telling the user to check their email.
5. The user's `confirmed_at` is not changed.

### Visitor requests a magic link with an unrecognised email (open registration)

1. Visitor submits an email that does not match any user.
2. System verifies the instance allows open registration and the email domain is acceptable.
3. System creates a new user record with the email, a generated username/name, a random password, and a placeholder profile image; confirmation notification is suppressed.
4. System calls `send_magic_link!` and enqueues `Users::GenerateAiProfileImageWorker` for the new user.
5. System renders the confirmation view.

### Visitor requests a magic link on an invite-only instance

1. Visitor submits an email that does not match any existing user.
2. System detects that `ForemInstance.invitation_only?` is true.
3. System redirects to the sign-in page with the alert "Forem is invite-only." and does not create a user.

### User clicks a valid magic link

1. User opens the magic link URL (`GET /magic_links/:token`) within 20 minutes of it being sent.
2. System locates the user by `sign_in_token` and confirms the token is not expired.
3. If `confirmed_at` is blank, the system sets it to the current time.
4. System signs the user in and redirects to the root path.

### Visitor enters the code manually via the code entry page

1. Visitor navigates to `GET /magic_links/new?state=code` (or clicks "Already have a code?").
2. System renders the code-entry view instead of the email form.
3. Visitor types their token into the input field and submits.
4. Client-side JavaScript constructs the `GET /magic_links/:token` URL and navigates to it, triggering the sign-in flow above.

## Failures / Exceptions

- Submitting the form without an email raises `ActiveRecord::RecordNotFound` (via `not_found`).
- An expired or unknown token redirects to the sign-in page with the alert "Invalid or expired link".
- A new-user registration attempt with an unacceptable email domain redirects to the sign-in page with the user's validation error messages and no user is created.
- A signed-in user visiting `GET /magic_links/new` is redirected to the root path immediately.
