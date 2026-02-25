---
id: "01KJBH3QQCWPWMJJ2CF7CWV5A4"
name: "user_can_view_billing_information"
status: "draft"
---

## Related Files

- `app/controllers/users_controller.rb`
- `app/views/users/_billing.html.erb` (Template)
- `spec/requests/user/user_settings_spec.rb` (Test)

## Functional Overview

When an authenticated user navigates to the billing settings tab (`/settings/billing`), the system loads Stripe customer data for that user and renders the billing partial. If the user has no Stripe ID code, the page presents a form to add a credit card. If the user has a Stripe ID code set to the special value `"special"`, no Stripe API call is made and `@customer` remains nil. Otherwise, the system fetches the customer record from Stripe via `Payments::Customer.get` and makes it available to the template, which then displays current subscription status, saved payment cards with options to set a primary card or remove cards, and a Stripe Checkout widget to add another card.

## Design Intent

The `"special"` stripe code guard in `handle_billing_tab` allows test or privileged accounts to visit the billing page without triggering a live Stripe API call, preventing errors in environments where those accounts have no real Stripe records.

## Key Members

- `@customer` — the Stripe customer object fetched by `Payments::Customer.get`; nil when the user has no Stripe ID or the ID is `"special"`
- `current_user.stripe_id_code` — the user's Stripe customer identifier; drives which branch of the billing template is rendered
- `current_user.cached_base_subscriber?` — determines whether subscription status information is displayed

## Scenarios

### User with no Stripe account visits billing tab

1. Authenticated user navigates to `/settings/billing`.
2. The system detects the user has no `stripe_id_code`.
3. The billing page renders with an "Add credit card" button and a Stripe Checkout form, but no existing card information.

### User with a Stripe account visits billing tab

1. Authenticated user navigates to `/settings/billing`.
2. The system fetches the Stripe customer record using the user's `stripe_id_code`.
3. The billing page displays saved payment cards, each showing brand, last four digits, and expiry date.
4. The primary card shows a remove button; non-primary cards show both a "make primary" button and a remove button.
5. An "Add another card" Stripe Checkout form is also present at the bottom.

### Active subscriber sees subscription status

1. Authenticated user with a valid `stripe_id_code` and an active base subscription visits `/settings/billing`.
2. The system fetches the Stripe customer record.
3. The page shows an info notice displaying the current subscriber status label and a localized description for that status (for free, trial, or paying subscription states).

### User with "special" Stripe code visits billing tab

1. Authenticated user whose `stripe_id_code` is `"special"` navigates to `/settings/billing`.
2. The system skips the Stripe API call entirely and leaves `@customer` unset.
3. The billing page renders without making any external payment service request.

### Unauthenticated user attempts to visit billing tab

1. A visitor who is not signed in navigates to `/settings/billing`.
2. The system redirects them to the sign-up/login page.

## Failures / Exceptions

- If a `flash[:error]` is present when the page renders (e.g., after a failed Stripe card operation), the billing template displays a danger alert inside the credit card form section.
