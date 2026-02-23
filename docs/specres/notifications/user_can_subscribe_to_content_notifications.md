---
id: "01KJ15N9VC5VXN9692QKQRVF5E"
name: "user_can_subscribe_to_content_notifications"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/notification_subscriptions_controller.rb`
- `app/services/notification_subscriptions/subscribe.rb`
- `app/services/notification_subscriptions/unsubscribe.rb`
- `app/services/notification_subscriptions/update.rb`
- `app/models/notification_subscription.rb`
- `app/workers/notification_subscriptions/update_worker.rb`
- `spec/requests/notification_subscriptions_spec.rb` (Test)
- `spec/models/notification_subscription_spec.rb` (Test)
- `spec/services/notification_subscriptions/subscribe_spec.rb` (Test)
- `spec/services/notification_subscriptions/unsubscribe_spec.rb` (Test)
- `spec/services/notification_subscriptions/update_spec.rb` (Test)
- `spec/workers/notification_subscriptions/update_worker_spec.rb` (Test)
- `spec/factories/notification_subscriptions.rb` (Test)
- `app/javascript/CommentSubscription/CommentSubscription.jsx`
- `app/javascript/CommentSubscription/commentSubscriptionUtilities.jsx`
- `app/javascript/CommentSubscription/index.js`
- `app/javascript/CommentSubscription/__tests__/CommentSubscription.test.jsx` (Test)
- `app/javascript/CommentSubscription/__tests__/commentSubscriptionUtilities.test.js` (Test)
- `app/javascript/CommentSubscription/__stories__/CommentSubscription.stories.jsx`

## Functional Overview

Authenticated users can subscribe to or unsubscribe from comment notifications on articles and comments. A `NotificationSubscription` record links a user to a notifiable resource (either an `Article` or a `Comment`) with a configuration value that controls which notifications are delivered (`all_comments`, `top_level_comments`, or `only_author_comments`). Subscriptions are unique per user per notifiable resource. The controller exposes four actions: a read endpoint to check current subscription state, a create endpoint via `NotificationSubscriptions::Subscribe` (idempotent — returns the existing record rather than raising a uniqueness error), a destroy endpoint via `NotificationSubscriptions::Unsubscribe`, and an upsert endpoint that handles both creating and removing subscriptions while also toggling the notifiable's `receive_notifications` flag when the acting user is the content author. When an article's authorship changes, `NotificationSubscriptions::UpdateWorker` runs asynchronously via Sidekiq to reassign all existing subscriptions to the new author. On the frontend, the `CommentSubscription` Preact component renders a Subscribe/Unsubscribe button group with a settings dropdown that lets users select their preferred subscription type (`all_comments`, `top_level_comments`, or `only_author_comments`) directly on the article page. The `commentSubscriptionUtilities` module handles the HTTP calls to read and update subscription state from the backend, translating responses into user-friendly status messages.

## Design Intent

The `create` action and `NotificationSubscriptions::Subscribe` are intentionally idempotent: the client may issue duplicate subscribe requests, so the system returns the existing subscription instead of raising a uniqueness validation error. The `upsert` action serves UI flows (e.g., a toggle in a dashboard) that need a single endpoint to both create and remove subscriptions, whereas `create`/`destroy` serve programmatic API consumers that prefer explicit intent. Cascade deletion of subscriptions when the owning user or article is destroyed is handled at the database level (`dependent: :delete`), bypassing ActiveRecord callbacks deliberately to avoid performance overhead.

## Key Members

- `config` — Controls which comment events trigger a notification: `all_comments`, `top_level_comments`, or `only_author_comments`. Defaults to `all_comments` when not specified.
- `notifiable_type` — Polymorphic discriminator; only `Article` and `Comment` are valid values.
- `receive_notifications` — Boolean flag on the notifiable record; toggled when the subscribing or unsubscribing user is the original author of that content.

## Scenarios

### Checking current subscription state

1. An authenticated user sends a GET request to `/notification_subscriptions/:notifiable_type/:notifiable_id`.
2. The system looks up any `NotificationSubscription` for that user and notifiable resource.
3. If a subscription exists, the response contains the `config` value (e.g., `"all_comments"`). If not, `config` is returned as `"not_subscribed"`.
4. For unauthenticated requests, the response body is `null`.

### Subscribing to notifications (create)

1. An authenticated user sends a POST request to `/comments/subscribe` with a `comment_id` or `article_id`, and optionally a `subscription_config`.
2. Authorization is checked via the `subscribe?` policy.
3. `NotificationSubscriptions::Subscribe` looks up the target `Comment` or `Article`. If neither is found, it raises `ArgumentError`.
4. The service calls `find_or_initialize_by` with the user, config, and notifiable. If a matching record already exists it is returned unchanged (idempotent); otherwise the new record is saved.
5. The result hash is rendered as JSON with HTTP 200.

### Unsubscribing from notifications (destroy)

1. An authenticated user sends a POST request to `/subscription/unsubscribe` with a `subscription_id`.
2. Authorization is checked via the `unsubscribe?` policy.
3. `NotificationSubscriptions::Unsubscribe` looks up the subscription by ID scoped to the current user.
4. If found, the record is destroyed and `{ destroyed: true }` is returned. If the subscription is not found or no ID is provided, an error hash is returned instead.

### Upserting a subscription via the dashboard (upsert)

1. An authenticated user sends a POST request to `/notification_subscriptions/:notifiable_type/:notifiable_id` with a `config` param.
2. If `config` is `"not_subscribed"`, the existing subscription record is deleted. If the user is the author of the notifiable content, `receive_notifications` on that record is set to `false`.
3. Otherwise, the subscription's `config` is set to the given value (defaulting to `"all_comments"`) and the record is saved. If the config is `"all_comments"` and the user is the author, `receive_notifications` is set to `true`.
4. JSON requests receive a boolean indicating whether the subscription is now persisted; HTML requests are redirected to the referrer.

### Updating subscriptions after authorship reassignment (background job)

1. When an article's authorship changes, `NotificationSubscription.update_notification_subscriptions` enqueues `NotificationSubscriptions::UpdateWorker` asynchronously via Sidekiq.
2. The worker validates that the notifiable class is `Article`; any other class raises `InvalidNotifiableForUpdate`.
3. If the article record cannot be found, the job returns early without error.
4. `NotificationSubscriptions::Update` bulk-updates all subscription records for that article, assigning them to the new author's user ID.

## Failures / Exceptions

- `NotificationSubscriptions::Subscribe` raises `ArgumentError` with the message `"missing notifiable"` if neither a valid `comment_id` nor `article_id` is supplied.
- `NotificationSubscriptions::Subscribe` returns `{ errors: <message> }` when saving fails (e.g., invalid `config` value).
- `NotificationSubscriptions::Unsubscribe` returns `{ errors: "Subscription ID is missing" }` when `subscription_id` is `nil`.
- `NotificationSubscriptions::Unsubscribe` returns `{ errors: "Notification subscription not found" }` when no subscription matching the given ID and current user exists.
- `NotificationSubscriptions::UpdateWorker` raises `InvalidNotifiableForUpdate` if the notifiable class is not in the permitted list (`Article`).
- The `upsert` action raises a 404 (`not_found`) when no user is signed in.
