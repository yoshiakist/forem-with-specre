---
id: "01KJVDW17MZNP820R66MDD04E5"
name: "user_can_subscribe_via_stripe_checkout"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stripe_subscriptions_controller.rb`
- `app/policies/stripe_subscription_policy.rb`
- `app/views/users/_billing.html.erb` (Template)
- `spec/requests/stripe_subscriptions_spec.rb` (Test)

## Functional Overview

When an authenticated user visits the new subscription path, the system creates a Stripe Checkout Session and immediately redirects the user to Stripe's hosted checkout page. The item code used for the session depends on the user's role and the request parameters: tag moderators are always directed to a dedicated moderator pricing item, regular users may supply a custom item code via a query parameter (as long as it does not match the tag-moderator code), and all other cases fall back to the platform's default base item code. The checkout session is configured with quantity 1, promotion-code support enabled, required terms-of-service consent, the user's email pre-filled, and the user's ID stored in session metadata for webhook reconciliation. After Stripe processes the purchase, the user is returned to a configurable success or cancel URL.

## Design Intent

Keeping item code selection entirely server-side prevents clients from freely substituting arbitrary price IDs. Tag moderators receive a privileged price automatically without needing to pass any parameter, ensuring they cannot accidentally (or deliberately) subscribe at a lower tier.

## Key Members

- `STRIPE_BASE_ITEM_CODE` — environment variable holding the default Stripe price ID used when no other code applies
- `STRIPE_TAG_MODERATOR_ITEM_CODE` — environment variable holding the price ID reserved for tag moderators
- `SUBSCRIPTION_SUCCESS_URL` / `SUBSCRIPTION_CANCEL_URL` — environment variables for post-checkout redirect destinations; default to `/settings/billing`
- `params[:item]` — optional query parameter allowing callers to request a specific price ID (ignored if it matches the tag-moderator code)
- `params[:mode]` — optional query parameter for the Stripe Checkout mode (defaults to `"subscription"`)

## Scenarios

### Unauthenticated user attempts to start checkout

1. A visitor who is not signed in requests the new subscription path.
2. The system's authentication guard redirects them to the sign-in page before any Stripe API call is made.

### Tag moderator initiates checkout

1. A signed-in user with the tag-moderator role requests the new subscription path.
2. The system detects the moderator role and selects the tag-moderator price ID, ignoring any `item` query parameter.
3. A Stripe Checkout Session is created with that price, mode `"subscription"`, promotion codes allowed, terms-of-service consent required, the user's email, and the user's ID in metadata.
4. The user is redirected to the Stripe-hosted checkout URL.

### Regular user initiates checkout with a custom item code

1. A signed-in, non-moderator user requests the new subscription path with a custom `item` query parameter that differs from the tag-moderator code.
2. The system uses the supplied item code as the price ID.
3. A Stripe Checkout Session is created with that price and the standard session parameters.
4. The user is redirected to the Stripe-hosted checkout URL.

### Regular user initiates checkout with the default item code

1. A signed-in, non-moderator user requests the new subscription path without providing an `item` parameter (or provides one that matches the tag-moderator code).
2. The system falls back to the base item code configured via `STRIPE_BASE_ITEM_CODE`.
3. A Stripe Checkout Session is created with that price and the standard session parameters.
4. The user is redirected to the Stripe-hosted checkout URL.

### Custom checkout mode is requested

1. A signed-in user requests the new subscription path with a `mode` query parameter (e.g., `"payment"`).
2. The system passes that mode value directly to the Stripe Checkout Session instead of the default `"subscription"` mode.
3. The user is redirected to the Stripe-hosted checkout URL for that mode.
