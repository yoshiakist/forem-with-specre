---
id: "01KJVE4GNV49HXNQ53W5PDJ31Z"
name: "user_can_remove_stripe_payment_card"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stripe_active_cards_controller.rb`
- `app/services/payments/customer.rb`
- `app/errors/payments.rb`
- `app/policies/stripe_active_card_policy.rb`
- `spec/requests/stripe_active_cards_spec.rb` (Test)
- `spec/services/payments/customer_spec.rb` (Test)
- `spec/policies/stripe_active_card_policy_spec.rb` (Test)
- `app/views/users/_billing.html.erb` (Template)

## Functional Overview

An authenticated user may remove a saved Stripe payment card from their account via a DELETE request to `/stripe_active_cards/:id`. Before detaching the card, the system verifies that the user's Stripe customer record has no active subscriptions; if any subscription exists, the request is rejected with an error message and the card is left untouched. When removal is permitted, the card source is detached from the Stripe customer, the customer record is saved, and an audit log entry is created under the `user.credit_card.edit` category. The user is always redirected back to the billing settings page, with either a success notice or an error flash.

## Scenarios

### Successful card removal

1. Authenticated user clicks the "Remove" button next to a payment card on the billing settings page.
2. Browser sends `DELETE /stripe_active_cards/:card_id`.
3. System checks the user's Stripe customer for active subscriptions and finds none.
4. System retrieves the card source from the Stripe customer, detaches it via the Stripe API, and saves the updated customer.
5. An `AuditLog` entry is created with slug `credit_card_remove` under category `user.credit_card.edit`.
6. User is redirected to billing settings with a success flash notice confirming removal.

### Removal blocked by active subscription

1. User attempts to delete a card while their Stripe customer has one or more active subscriptions.
2. System detects that `customer.subscriptions.count` is greater than zero.
3. No detach call is made to Stripe; the card remains on the account.
4. User is redirected to billing settings with an error flash message instructing them to cancel their membership first.

### Removal fails due to unknown card ID

1. User sends `DELETE /stripe_active_cards/unknown` with a card ID that does not exist on their Stripe customer.
2. System attempts to retrieve the source and Stripe raises `Stripe::InvalidRequestError`.
3. The error is wrapped as `Payments::InvalidRequestError` and a Datadog counter at `stripe.errors` is incremented.
4. User is redirected to billing settings with the Stripe error message shown in the error flash.

## Failures / Exceptions

- **Active subscription guard:** If `customer.subscriptions.count > 0`, the destroy action sets an error flash ("Can't remove card if you have an active membership. Please cancel your membership first.") and redirects without touching Stripe.
- **Unknown source ID:** `Payments::Customer.get_source` raises `Payments::InvalidRequestError` when the card ID is not found; the controller rescues this, increments `stripe.errors` in Datadog, and redirects with the error message.
- **Authorization:** `StripeActiveCardPolicy#destroy?` always returns `true`, so all authenticated users are authorized. Unauthenticated requests are blocked by `authenticate_user!`.
- **Stripe API errors:** Any `Stripe::InvalidRequestError` propagated through `Payments::Customer` methods is re-raised as `Payments::InvalidRequestError` and caught by the controller's rescue clause.
