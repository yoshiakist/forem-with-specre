---
id: "01KJVE2459NGVYNN0C6XT6TMSM"
name: "user_can_cancel_stripe_subscription"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stripe_subscriptions_controller.rb`
- `app/policies/stripe_subscription_policy.rb`
- `spec/requests/stripe_subscriptions_spec.rb` (Test)
- `app/views/users/_billing.html.erb` (Template)

## Functional Overview

An authenticated user can cancel their active Stripe subscription by submitting a DELETE request with the exact verification string "pleasecancelmyplusplus". The system confirms the user has a Stripe customer ID on record, retrieves their active subscription from Stripe, cancels it immediately by setting cancel_at_period_end to false, removes the `base_subscriber` role from the user, and redirects back with a success notice. If the verification string is wrong, no Stripe customer ID is found, or no active subscription exists, the request is rejected with an appropriate error message and no changes are made.

## Scenarios

### Successful cancellation

1. A signed-in user submits a DELETE request to the subscription endpoint with the verification parameter set to "pleasecancelmyplusplus".
2. The system confirms the user has a Stripe customer ID on file.
3. The system fetches the first active subscription associated with that customer from Stripe.
4. The system updates the subscription to cancel immediately (cancel_at_period_end: false).
5. The system removes the `base_subscriber` role from the user and touches the user and profile records.
6. The user is redirected back with a success flash notice: "Your subscription has been canceled."

### Cancellation blocked by wrong verification string

1. A signed-in user submits a DELETE request with an incorrect verification parameter (anything other than "pleasecancelmyplusplus").
2. The user has a Stripe customer ID on file.
3. The system skips all Stripe API calls and makes no changes.
4. The user is redirected back with an error flash: "Invalid verification parameter. Subscription was not canceled."

### Cancellation blocked when no Stripe customer ID exists

1. A signed-in user submits a DELETE request with any verification parameter.
2. The user has no Stripe customer ID on file.
3. The system skips all Stripe API calls and makes no changes.
4. The user is redirected back with an error flash: "No active subscription found. Please contact us if you believe this is an error."

### Cancellation blocked when no active subscription is found in Stripe

1. A signed-in user submits a DELETE request with the correct verification parameter.
2. The user has a Stripe customer ID on file, but querying Stripe returns no subscriptions for that customer.
3. The system makes no changes and removes no roles.
4. The user is redirected back with an error flash: "No active subscription found."

## Failures / Exceptions

- Wrong verification string with a valid Stripe customer ID: returns error "Invalid verification parameter. Subscription was not canceled."
- No Stripe customer ID on the user record (regardless of verification): returns error "No active subscription found. Please contact us if you believe this is an error."
- Correct verification string and a valid Stripe customer ID, but no subscription exists in Stripe: returns error "No active subscription found."
- Unauthenticated request: redirected to the sign-in page before the action is reached.
