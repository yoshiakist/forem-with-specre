---
id: "01KJVDW6ZPBBC4Y26Z8YE18P1G"
name: "system_processes_stripe_subscription_webhooks"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/incoming_webhooks/stripe_events_controller.rb`
- `spec/requests/incoming_webhooks/stripe/stripe_events_spec.rb` (Test)

## Functional Overview

The `IncomingWebhooks::StripeEventsController` receives POST requests from Stripe's webhook delivery system, verifies the request signature using the configured signing secret, and dispatches to one of four event-specific handlers based on the event type. The handled event types are `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, and `customer.subscription.deleted`. Each handler extracts the user ID from the event's metadata, looks up the user, and updates their subscriber role and status accordingly. On successful processing of any event type, the controller responds with `{ status: "success" }` and HTTP 200. Unrecognized event types are logged and silently ignored.

## Scenarios

### Checkout session completed — new subscriber

1. Stripe delivers a `checkout.session.completed` event with the user's ID in the session metadata.
2. The controller verifies the webhook signature and parses the event.
3. If the user is not yet a `base_subscriber`, the system grants that role, records the Stripe customer ID on the user, sets the subscriber status to `paying_subscription` (or `trial_subscription` if trial period days are present), and sends the base subscriber role email via `NotifyMailer`.
4. The system looks for billboard click events belonging to that user created within the past 3 hours. For each such event, it creates a corresponding `conversion` billboard event preserving the geolocation, context type, and billboard ID.
5. The controller responds with HTTP 200.

### Subscription created

1. Stripe delivers a `customer.subscription.created` event with the user's ID in the subscription metadata.
2. The controller verifies the signature and parses the event.
3. If the user does not yet have the `base_subscriber` role, that role is added.
4. The subscriber status is set based on the subscription's Stripe status (`trialing` → `trial_subscription`, `active` with zero price → `free_subscription`, `active` with non-zero price → `paying_subscription`, otherwise `not_subscribed`).
5. The controller responds with HTTP 200.

### Subscription updated — cancellation scheduled

1. Stripe delivers a `customer.subscription.updated` event where the metadata field `cancel_at_period_end` is `true`.
2. The controller verifies the signature and parses the event.
3. The system adds the `impending_base_subscriber_cancellation` role to the user (if not already present) and updates their subscriber status using the standard status determination logic.
4. The controller responds with HTTP 200.

### Subscription updated — cancellation reversed

1. Stripe delivers a `customer.subscription.updated` event where `cancel_at_period_end` is not `true`.
2. The controller verifies the signature and parses the event.
3. The system ensures the user has the `base_subscriber` role and updates their subscriber status.
4. The controller responds with HTTP 200.

### Subscription deleted

1. Stripe delivers a `customer.subscription.deleted` event with the user's ID in the subscription metadata.
2. The controller verifies the signature and parses the event.
3. The system adds the `impending_base_subscriber_cancellation` role to the user (if not already present) and sets the subscriber status to `not_subscribed`.
4. The controller responds with HTTP 200.

## Failures / Exceptions

- If the request body is not valid JSON, the controller rescues `JSON::ParserError`, logs the error, and responds with HTTP 400 and an error message.
- If the Stripe signature cannot be verified (e.g., tampered payload, wrong secret), the controller rescues `Stripe::SignatureVerificationError`, logs the error, and responds with HTTP 400 and an error message.
- If the event metadata does not contain a `user_id`, or no user is found for that ID, the handler returns early without making any changes.
- Errors during Stripe customer ID extraction are caught and reported to Honeybadger, returning `nil` rather than propagating.
