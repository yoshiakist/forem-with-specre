---
id: "01KJVE2B3BE3E5GX1FAFCMEAEV"
name: "user_can_set_default_payment_card"
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

An authenticated user with multiple saved payment cards can designate any of them as their default payment source. The billing settings page renders each non-default card with a "Make primary" button that submits a PATCH request to `PATCH /stripe_active_cards/:card_id`. The controller retrieves the Stripe customer record, looks up the requested card source, sets it as the customer's `default_source`, and persists the change through `Payments::Customer.save`. On success a settings notice flash is shown and an `AuditLog` entry is recorded. Authorization is enforced by `StripeActiveCardPolicy`, which blocks suspended or spam users from making changes.

## Scenarios

### User sets a non-default card as the default

1. User navigates to the billing settings page; multiple saved cards are displayed.
2. User clicks "Make primary" on any card that is not already the default.
3. Browser submits `PATCH /stripe_active_cards/:card_id` for that card.
4. System retrieves the Stripe customer via the user's `stripe_id_code`, then retrieves the specific card source by the given ID.
5. System sets `customer.default_source` to the retrieved card's ID and calls `Payments::Customer.save`.
6. On success, the user is redirected to the billing settings page with a "Your billing information has been updated" notice, and an `AuditLog` entry with slug `credit_card_update` is created.

### Authorization blocks suspended or spam users

1. A suspended or spam-flagged user attempts `PATCH /stripe_active_cards/:card_id`.
2. `StripeActiveCardPolicy#update?` returns `false`.
3. Pundit raises `NotAuthorizedError` and the request is denied before the Stripe API is called.

## Failures / Exceptions

- **Unknown card ID** — If the supplied card ID does not exist on the customer, `Payments::Customer.get_source` raises `Payments::InvalidRequestError`. The controller rescues it, increments `stripe.errors` in Datadog with tags `action:update_card` and `user_id:<id>`, and redirects the user to the billing page with the Stripe error message in the flash.
- **Card error from Stripe** — A `Stripe::CardError` during the request is wrapped in `Payments::CardError` and handled the same way: error incremented in Datadog and the user redirected with the error message.
- **Save failure (non-exception)** — If `Payments::Customer.save` returns a falsy value without raising, the controller does not create an audit log, increments `stripe.errors` tagged `action:update_card`, and sets `flash[:error]` to the "cannot update" i18n message before redirecting.
