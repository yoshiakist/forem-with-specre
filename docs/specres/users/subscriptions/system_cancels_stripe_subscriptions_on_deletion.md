---
id: "01KJA13RFHYRH8PKETC8250A61"
name: "system_cancels_stripe_subscriptions_on_deletion"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/services/users/cancel_stripe_subscriptions.rb`
- `spec/services/users/cancel_stripe_subscriptions_spec.rb` (Test)

## Functional Overview

When a user account is being deleted, the system cancels all of the user's active Stripe subscriptions before the account is removed. `Users::CancelStripeSubscriptions` looks up the user's Stripe customer ID, retrieves all active subscriptions from the Stripe API, and cancels each one immediately (not at period end). If the user has no Stripe customer ID or is nil, the service exits silently. All Stripe API errors are caught and logged without re-raising, so that a Stripe failure never blocks account deletion. Successful cancellations and failures are both tracked via logging and metrics.

## Design Intent

The service is designed to be resilient — every Stripe API call is wrapped in error handling so that account deletion always proceeds even if the Stripe integration is unavailable or the customer no longer exists in Stripe. Individual subscription cancellations are isolated so that one failure does not prevent cancelling the remaining subscriptions.

## Key Members

- `user` — the user whose Stripe subscriptions are being cancelled; must have a `stripe_id_code` for any action to be taken.

## Scenarios

### Cancelling active subscriptions for a user with a Stripe account

1. The system receives a user with a valid Stripe customer ID.
2. It sets the Stripe API key and lists all active subscriptions for that customer.
3. For each subscription, the system updates it to cancel immediately (not at period end).
4. Each successful cancellation is logged and a metrics counter is incremented.

### User has no Stripe customer ID

1. The system receives a user whose Stripe customer ID is blank or nil.
2. The service returns immediately without making any Stripe API calls.

### User is nil

1. The system receives a nil user reference.
2. The service returns immediately without making any Stripe API calls.

### Stripe API returns an error when listing subscriptions

1. The system attempts to list active subscriptions but Stripe returns an invalid-request error (e.g., customer not found).
2. The error is logged but not re-raised, so account deletion continues unimpeded.

### Individual subscription cancellation fails

1. The system successfully lists active subscriptions but a specific subscription update fails with a Stripe error.
2. The error for that subscription is logged, and the system continues attempting to cancel the remaining subscriptions.

## Failures / Exceptions

- Stripe customer not found — logged as an invalid-request error, not re-raised.
- Individual subscription update fails — logged, does not block other cancellations.
- Unexpected errors — caught at the top level, logged, reported to error tracker, and metrics incremented; never re-raised.
