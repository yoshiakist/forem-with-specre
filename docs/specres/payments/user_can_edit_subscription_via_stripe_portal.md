---
id: "01KJVDZ0VWPAMMPR1QMC4D1Q8P"
name: "user_can_edit_subscription_via_stripe_portal"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stripe_subscriptions_controller.rb`
- `app/policies/stripe_subscription_policy.rb`
- `app/views/users/_billing.html.erb` (Template)
- `spec/requests/stripe_subscriptions_spec.rb` (Test)

## Functional Overview

An authenticated user who already holds a Stripe subscription can access the Stripe Billing Portal to self-manage their subscription. When the user triggers the edit action, the system looks up the user's stored Stripe customer ID and creates a Billing Portal session via the Stripe API. The user is then immediately redirected to the hosted portal URL. If the user has no stored Stripe customer ID, the system surfaces a flash error message and redirects them back to the settings page, prompting them to contact support instead.

## Design Intent

The portal session delegates all subscription-management UI to Stripe's hosted Billing Portal, keeping billing logic out of the application. The return URL brings the user back to the settings billing page after they finish in the portal.

## Scenarios

### Authenticated user with a Stripe customer ID opens the portal

1. User navigates to the edit subscription path while signed in.
2. The system reads the user's stored Stripe customer ID.
3. The system creates a `Stripe::BillingPortal::Session` for that customer, with the billing settings page as the return URL.
4. The user is redirected to the portal session URL on Stripe's domain.

### Authenticated user without a Stripe customer ID attempts to open the portal

1. User navigates to the edit subscription path while signed in.
2. The system finds no Stripe customer ID on the user record.
3. The system sets a flash error: "Unable to edit subscription self-serve. Please contact support."
4. The user is redirected back to their settings page.

### Unauthenticated user attempts to access the portal

1. Unauthenticated visitor requests the edit subscription path.
2. The `authenticate_user!` before-action intercepts the request.
3. The visitor is redirected to the sign-in page.

## Failures / Exceptions

- If `current_user.stripe_id_code` is blank, the system does not call the Stripe API and instead redirects back with a flash error message directing the user to contact support.
