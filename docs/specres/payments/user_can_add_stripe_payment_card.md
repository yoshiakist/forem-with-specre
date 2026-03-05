---
id: "01KJVDZDG8Y04Z6WRBBRCDEZGF"
name: "user_can_add_stripe_payment_card"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stripe_active_cards_controller.rb`
- `app/services/payments/customer.rb`
- `app/errors/payments.rb`
- `app/policies/stripe_active_card_policy.rb`
- `app/views/users/_billing.html.erb` (Template)
- `spec/requests/stripe_active_cards_spec.rb` (Test)
- `spec/services/payments/customer_spec.rb` (Test)
- `spec/policies/stripe_active_card_policy_spec.rb` (Test)

## Functional Overview

An authenticated, non-suspended user can add a credit card to their account via the Stripe Checkout popup on the billing settings page. The browser collects the card details and exchanges them for a short-lived Stripe token, which is submitted to `POST /stripe_active_cards`. The controller authorizes the request via `StripeActiveCardPolicy`, then finds or creates a Stripe customer record for the user (persisting the resulting `stripe_id_code` on first creation). It delegates to `Payments::Customer.create_source` to attach the tokenized card to the Stripe customer. On success, a flash notice is shown and an `AuditLog` entry is created with category `user.credit_card.edit`. On failure, an error metric is emitted to Datadog and the user is redirected back to the billing page with an error message.

## Design Intent

The controller never handles raw card numbers; it only receives a Stripe token produced by Stripe Checkout in the browser, keeping PCI scope minimal. Stripe API errors are wrapped in custom `Payments::CardError` and `Payments::InvalidRequestError` classes so callers are insulated from Stripe SDK internals.

## Key Members

- `stripe_token` — the only permitted request parameter; a short-lived Stripe token representing the card entered in the browser popup.
- `stripe_id_code` (on `User`) — the Stripe customer ID stored on the user record, created on first card addition if absent.
- `AUDIT_LOG_CATEGORY` — `"user.credit_card.edit"`, used for all audit log entries in this controller.

## Scenarios

### User adds a card when no Stripe customer exists yet

1. Authenticated user with no `stripe_id_code` visits the billing settings page and sees an "Add credit card" button.
2. User clicks the button; the Stripe Checkout popup opens pre-filled with their email address.
3. User enters valid card details; Stripe returns a token to the browser callback.
4. The browser submits the token as `stripe_token` via a POST form to `/stripe_active_cards`.
5. The controller calls `Payments::Customer.create` to create a new Stripe customer and stores the returned customer ID as `stripe_id_code` on the user record.
6. The controller attaches the card token to the new customer via `Payments::Customer.create_source`.
7. A success flash notice is displayed, an `AuditLog` entry is created, and the user is redirected to the billing settings page.

### User adds an additional card when a Stripe customer already exists

1. Authenticated user who already has a `stripe_id_code` visits billing settings; existing cards are listed.
2. User clicks "Add another card" and completes the Stripe Checkout popup to obtain a new token.
3. The controller retrieves the existing Stripe customer via `Payments::Customer.get`.
4. The new card token is attached as a source to the existing customer.
5. A success flash notice is displayed, an `AuditLog` entry is created, and the user is redirected to the billing settings page.

### Card addition fails due to an invalid card

1. User submits a Stripe token that Stripe rejects (e.g., incorrect card number).
2. `Payments::Customer.create_source` raises `Payments::CardError`.
3. The controller increments the `stripe.errors` metric in Datadog with tags identifying the action and user.
4. The user is redirected to the billing settings page with the error message from Stripe displayed in a flash alert.

### Card addition fails due to an invalid request parameter

1. A `Stripe::InvalidRequestError` is raised during customer creation or source creation (e.g., malformed token).
2. The error is wrapped as `Payments::InvalidRequestError` and re-raised.
3. The controller rescues it, increments the `stripe.errors` metric in Datadog, and redirects to the billing page with the error message in a flash alert.

### Suspended or spam user is denied

1. A user flagged as spam or suspended attempts to POST to `/stripe_active_cards`.
2. `StripeActiveCardPolicy#create?` returns `false`.
3. Pundit raises `Pundit::NotAuthorizedError` and the request is rejected.

## Failures / Exceptions

- `Payments::CardError` — raised when Stripe rejects the card (e.g., incorrect number, insufficient funds). Caught by the controller; redirects to billing page with Stripe's error message.
- `Payments::InvalidRequestError` — raised when a Stripe API request is malformed (e.g., bad token format). Caught by the controller; redirects with Stripe's error message.
- `Payments::PaymentsError` — base class for both errors above; also raised for unexpected `Stripe::StripeError` instances, which are additionally reported to Honeybadger.
- On any failure the `stripe.errors` Datadog counter is incremented with tags `action:create_card` and `user_id:<id>`.
