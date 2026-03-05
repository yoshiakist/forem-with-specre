---
id: "01KJBEKF5TEFAMMCQ7T6X9A6DV"
name: "user_can_request_account_deletion"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/users_controller.rb`
- `app/services/users/request_destroy.rb`
- `spec/requests/user/user_destroy_spec.rb` (Test)
- `app/views/users/confirm_destroy.html.erb` (Template)

## Functional Overview

An authenticated user with a verified email address can initiate account deletion by posting to the `request_destroy` endpoint. The system generates a short-lived, one-time token stored in the cache for 12 hours, then delivers a confirmation email containing the token. If a deletion request is already in progress (i.e., a token is already cached for the user), the system notifies the user without sending a new email. Users without an email address cannot initiate the flow and are directed to add one first. After clicking the link in the email, the user lands on a confirmation page (`confirm_destroy`) where they must type their username and the word "DELETE" before the final deletion is submitted.

## Design Intent

The two-step token flow (request then confirm via email link) prevents accidental or unauthorized deletions: possession of the confirmation email is treated as proof of identity. Storing the token in the cache rather than the database keeps the token ephemeral and makes expiry automatic, avoiding orphaned records. A duplicate-request guard prevents token churn and avoids spamming the user with multiple emails.

## Key Members

- `destroy_token` — a 20-character hex string written to `Rails.cache` under the key `user-destroy-token-<user_id>`, with a 12-hour TTL. Used as the single-use confirmation credential.

## Scenarios

### User successfully requests account deletion

1. An authenticated user with a registered email address submits a deletion request.
2. The system checks that no deletion token already exists in the cache for this user.
3. A random token is generated and written to the cache with a 12-hour expiry.
4. The system sends an `account_deletion_requested_email` to the user containing the token.
5. The user is redirected to their account settings page with a notice confirming the request was received.

### Request is blocked when a deletion is already in progress

1. An authenticated user submits a deletion request, but a token for their account is already present in the cache.
2. The system does not generate a new token or send a new email.
3. The user is redirected to account settings with a notice indicating that a deletion request is already in progress.

### User without an email cannot request deletion

1. An authenticated user whose account has no email address submits a deletion request.
2. The system redirects the user to account settings with a notice asking them to provide an email address first.

### User confirms deletion with a valid token

1. The user clicks the confirmation link from the email, which includes their token as a query parameter.
2. The system reads the stored token from the cache and compares it to the token in the URL.
3. The tokens match, so the `confirm_destroy` page is rendered, presenting a form that requires the user to type their username and "DELETE" before proceeding.

### Confirmation fails due to an expired or mismatched token

1. The user visits the confirmation URL, but the cache entry has expired (TTL elapsed).
2. The system redirects to account settings with a notice that the token has expired.
3. Alternatively, if a token exists in the cache but does not match the one in the URL, the system raises a routing error and returns a Not Found response.

### Unauthenticated user visits the confirmation page

1. A visitor who is not signed in follows the confirmation link.
2. The system redirects them to the sign-up page with an alert asking them to log in before deleting their account.

## Failures / Exceptions

- If the cache token is absent (expired), the user is redirected to account settings with an expiry notice rather than shown the confirmation page.
- If the URL token does not match the cached token, a `ActionController::RoutingError` (404) is raised. Mismatched token values are forwarded to Honeycomb for observability.
- If the user has no email at the time of triggering `full_delete`, they are redirected to account settings without scheduling the deletion worker.
