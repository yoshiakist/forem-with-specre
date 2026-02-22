---
id: "01KJ2SF6J4K95BTZRSZG5AA811"
name: "user_can_purchase_credits"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/credits_controller.rb`
- `app/services/payments/process_credit_purchase.rb`
- `app/models/credit.rb`
- `app/assets/javascripts/initializers/initializeCreditsPage.js`
- `app/views/credits/new.html.erb` (Template)
- `app/views/credits/_pricing.en.html.erb` (Template)
- `app/views/credits/_pricing.fr.html.erb` (Template)
- `app/views/credits/_pricing.pt.html.erb` (Template)
- `app/views/credits/_purchase_faq.en.html.erb` (Template)
- `app/views/credits/_purchase_faq.fr.html.erb` (Template)
- `app/views/credits/_purchase_faq.pt.html.erb` (Template)
- `spec/requests/credits_spec.rb` (Test)
- `spec/services/payments/process_credit_purchase_spec.rb` (Test)
- `spec/views/credits/new.html.erb_spec.rb` (Test)

## Functional Overview

Authenticated users can purchase platform credits in bulk via a Stripe-backed checkout flow. The purchase page (`GET /credits/purchase`) shows tiered pricing, the user's current credit balance, and a Stripe card input or previously saved cards. On form submission (`POST /credits`), the server delegates to `Payments::ProcessCreditPurchase`, which finds or creates a Stripe customer, attaches the payment card, charges the computed amount, and bulk-inserts the purchased credits for the purchasing party (a user or an organization admin is purchasing on behalf of their org). On success the user is redirected to the credits ledger; on failure the error message is surfaced and the purchase form is re-displayed.

## Design Intent

The service uses Stripe's legacy checkout API intentionally. The team evaluated Stripe's newer API (which supports SCA) but determined the legacy API was sufficient for occasional one-off purchases. This decision is documented in the internal engineering issue linked in the service file's comment.

Pricing uses four volume tiers (small, medium, large, xlarge) sourced from `Settings::General.credit_prices_in_cents`, keeping pricing configurable without code changes. Credits are inserted with `Credit.insert_all` rather than one-by-one `create` calls to minimize database round-trips when purchasing large quantities.

## Key Members

- `purchase_options[:stripe_token]` — a one-time Stripe card token for a new card
- `purchase_options[:selected_card]` — the ID of a previously saved Stripe card source
- `purchase_options[:organization_id]` — when present, credits are attributed to the organization rather than the individual user
- `credits_count` — the number of credits the user wishes to purchase; drives both the charge amount and the number of credit rows created

## Scenarios

### User purchases credits with a new card

1. An authenticated user navigates to `GET /credits/purchase`.
2. The page renders the tiered pricing grid, the user's current unspent credit balance, and an empty Stripe card input element.
3. The user enters the desired quantity and types card details into the Stripe element.
4. On submit, the browser collects the card via Stripe.js and injects the resulting `stripe_token` as a hidden field before submitting the form.
5. The server calls `Payments::ProcessCreditPurchase` with the user, the credit quantity, and the token.
6. The service finds or creates a Stripe customer, creates a new card source from the token, charges the total cost (quantity times the per-credit price for that tier), and bulk-inserts the credits attributed to the user.
7. The user is redirected to `GET /credits` with a success notice stating how many credits were added.

### User purchases credits with a previously saved card

1. An authenticated user with an existing Stripe customer record navigates to `GET /credits/purchase`.
2. The page lists their saved cards as radio buttons; a new-card form can be revealed on demand.
3. The user selects a saved card and submits the form with a `selected_card` parameter.
4. The service retrieves the existing card source from the Stripe customer and charges it for the computed amount.
5. Credits are created and the user is redirected to the credits ledger on success.

### Organization admin purchases credits on behalf of their organization

1. An authenticated org admin navigates to `GET /credits/purchase?organization_id=<id>`.
2. The controller verifies the user is an admin of the requested organization; if not, access is denied.
3. The page renders with the organization as the purchaser, allowing the admin to switch between personal and org purchase contexts via links.
4. On submit, the `organization_id` is sent as a hidden field.
5. The service creates credits attributed to the organization (not the individual user) and updates the organization's cached credit counts.
6. The admin is redirected to the ledger; no personal credits are created for them.

### Purchase fails due to a payment error

1. A user submits the purchase form with a valid card token and a desired quantity.
2. The Stripe charge raises a `Payments::PaymentsError` (e.g., card declined).
3. The service catches the error, sets its `error` message, and marks the purchase as unsuccessful.
4. No credits are created.
5. The controller re-displays the purchase form with the error message shown in a danger alert.

### Purchase fails because no payment method was provided

1. A user submits the form without providing a `stripe_token` or a `selected_card`.
2. The service detects that neither payment method option is present and sets an error without attempting a charge.
3. The controller redirects back to the purchase form and displays the error.

## Failures / Exceptions

- If no payment method (`stripe_token` or `selected_card`) is present, the service returns immediately with an error message rather than contacting Stripe.
- Any `Payments::PaymentsError` raised during customer lookup, card attachment, or charge creation is caught in `process_purchase`; the service transitions to a failed state and no credits are inserted.
- If an `organization_id` is provided but the current user is not an org admin for that organization, the controller calls `not_authorized` before the purchase service is invoked.
