---
id: "01KJ9RAX3Y386ZACHQ0XRZ8GWT"
name: "user_subscribes_to_author_content"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/user_subscriptions_controller.rb`
- `app/services/user_subscriptions/create_from_controller_params.rb`
- `app/models/concerns/user_subscription_sourceable.rb`
- `app/javascript/liquidTags/userSubscriptionLiquidTag.js`
- `app/models/user_subscription.rb` — Tagged: 01KJ1F6M9DTXAJNC4ZQFMSWJXE
- `spec/requests/user_subscriptions_spec.rb` (Test)
- `spec/services/user_subscriptions/create_from_controller_params_spec.rb` (Test)
- `spec/models/shared_examples/user_subscription_sourceable.rb` (Test)
- `spec/models/user_subscription_spec.rb` (Test)

## Functional Overview

When a signed-in user reads an article that includes a user-subscription liquid tag, a frontend widget is rendered that lets them subscribe to the author's future content. The liquid tag JS checks whether the user is already subscribed via `GET /user_subscriptions/subscribed`, then presents a confirmation modal before submitting a `POST /user_subscriptions` request with the article's `source_type` and `source_id`. The controller enforces authentication and rate limiting, then delegates to `UserSubscriptions::CreateFromControllerParams`, which validates that the `source_type` is allowlisted, that the source record exists and is active, and that the source has the user-subscription liquid tag enabled. If all checks pass, the service calls `build_user_subscription` on the source (provided by the `UserSubscriptionSourceable` concern) to construct and persist the record, linking the subscriber, the author, and the polymorphic source. Apple Auth users whose email is a private relay address are blocked at the model-validation level and receive a descriptive error.

## Design Intent

- **Rate limiting on creation:** Subscription creation is guarded by `rate_limit!(:user_subscription_creation)` and the count is tracked on success, preventing abuse without blocking legitimate users.
- **Apple Auth guard:** Users who signed up with Apple receive a private relay email (`@privaterelay.appleid.com`) that cannot receive external mail. The model rejects these at validation time so they are never stored, and the frontend detects the relay domain to show a friendly explanation before the user even attempts to subscribe.
- **Confirmation modal:** The frontend always shows a modal asking the user to confirm before POSTing the subscription, reducing accidental subscriptions.
- **Polymorphic source via concern:** `UserSubscriptionSourceable` is a reusable ActiveRecord concern that any model can include to become a subscription source, keeping the subscription logic decoupled from any specific content type.
- **Allowlist for source_type:** `UserSubscription::ALLOWED_TYPES` limits which models can act as sources, preventing arbitrary `constantize` calls on untrusted input.

## Key Members

- `source_type` — String identifying the content model (e.g., `"Article"`); must be in `UserSubscription::ALLOWED_TYPES`.
- `source_id` — Integer ID of the content record acting as the subscription source.
- `subscriber_email` — Email of the subscribing user, recorded at subscription time.
- `Response` (Struct) — Returned by `CreateFromControllerParams#call`; fields: `success` (Boolean), `data` (UserSubscription or nil), `error` (String or nil).
- `build_user_subscription(subscriber)` — Instance method on any `UserSubscriptionSourceable` model; builds (but does not save) a `UserSubscription` associating the source, the source's author, and the subscriber.

## Scenarios

### Successful subscription

1. A signed-in user opens an article containing the user-subscription liquid tag.
2. The frontend checks `GET /user_subscriptions/subscribed` with the article's source type and ID and receives `is_subscribed: false`.
3. The user clicks the subscribe button; a confirmation modal appears.
4. The user confirms; the frontend POSTs to `/user_subscriptions` with `source_type: "Article"`, `source_id`, and `subscriber_email`.
5. The controller verifies the user is authenticated, enforces the rate limit, and calls `CreateFromControllerParams`.
6. The service validates the source type, looks up the article, confirms it is active and has the liquid tag enabled, and saves the `UserSubscription`.
7. The controller responds with `{ message: "success", success: true }` and HTTP 200; the frontend updates all subscription widgets on the page to reflect the subscribed state.

### Invalid source type

1. A POST to `/user_subscriptions` is submitted with a `source_type` not in `UserSubscription::ALLOWED_TYPES` (e.g., `"Comment"`).
2. `CreateFromControllerParams` returns `success: false` and `error: "Invalid source_type."` without touching the database.
3. The controller responds with HTTP 422 and the error message.

### Apple Auth subscriber blocked

1. A user whose email ends with `@privaterelay.appleid.com` attempts to subscribe via the frontend.
2. The liquid tag JS detects the relay domain and prevents the subscription modal from appearing, showing an explanatory message instead.
3. If a POST is submitted regardless, the `UserSubscription` model validation rejects the private relay email, and the controller returns HTTP 422 with the error "Can't subscribe with an Apple private relay. Please update email."

### Rate-limited subscriber

1. A user exceeds the `user_subscription_creation` rate limit threshold.
2. The controller's `rate_limit!` call halts processing and returns HTTP 429 with a `Retry-After` header indicating when the user may try again.

### Already subscribed

1. A signed-in user returns to an article they previously subscribed to.
2. The frontend calls `GET /user_subscriptions/subscribed`; the controller returns `{ is_subscribed: true, success: true }`.
3. The widget renders in a "subscribed" state; no subscription modal is shown.
4. If a duplicate POST is submitted anyway, the `UserSubscription` model's uniqueness validation rejects it and the controller returns HTTP 422 with "Subscriber has already been taken."

## Failures / Exceptions

- `source_type` not in allowlist — HTTP 422, `"Invalid source_type."`
- Source record not found (bad ID or unpublished article) — HTTP 422, `"Source not found."` or `"Source not found. Please make sure your Article is active!"`
- Source does not have the user-subscription liquid tag enabled — HTTP 422, `"User subscriptions are not enabled for the source."`
- Apple private relay email — HTTP 422, `"Subscriber email Can't subscribe with an Apple private relay. Please update email."`
- Duplicate subscription — HTTP 422, `"Subscriber has already been taken"`
- Rate limit exceeded — HTTP 429 with `Retry-After` header
- Missing required params on `GET /subscribed` — raises `ActionController::ParameterMissing`
