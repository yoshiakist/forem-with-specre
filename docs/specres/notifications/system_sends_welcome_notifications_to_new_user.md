---
id: "01KJ15YPZ52QH5K5R1MVAYRQ0F"
name: "system_sends_welcome_notifications_to_new_user"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/welcome_notification/send.rb`
- `app/workers/notifications/welcome_notification_worker.rb`
- `app/services/broadcasts/welcome_notification/generator.rb`
- `app/workers/broadcasts/send_welcome_notifications_worker.rb`
- `app/models/welcome_notification.rb`
- `app/views/notifications/_broadcast.html.erb` (Template)
- `spec/services/notifications/welcome_notification/send_spec.rb` (Test)
- `spec/workers/notifications/welcome_notification_worker_spec.rb` (Test)
- `spec/services/broadcasts/welcome_notification/generator_spec.rb` (Test)
- `spec/workers/broadcasts/send_welcome_notifications_worker_spec.rb` (Test)

## Functional Overview

The system delivers a sequenced series of onboarding notifications to newly registered users over their first week on the platform. A scheduled worker (`Broadcasts::SendWelcomeNotificationsWorker`) runs periodically, iterates over users created after the feature's go-live date (up to 8 days ago), and invokes `Broadcasts::WelcomeNotification::Generator` for each eligible user. The generator checks that the user has not opted out of welcome notifications, then evaluates up to six contextual broadcast types in a fixed priority order, sending at most one notification per execution. Each notification is dispatched asynchronously via `Notifications::WelcomeNotificationWorker`, which verifies that the target broadcast is still active before calling `Notifications::WelcomeNotification::Send` to create the `Notification` record and log the event to Datadog. The broadcast type sent at each step depends on the user's account age, connected authentication providers, tag-follow activity, discussion history, and whether they have already received each notification type.

## Design Intent

At most one welcome notification is sent per user per execution of the generator. The `notification_enqueued` flag is set immediately after scheduling the first applicable notification, preventing further notification methods from running in the same pass. This ensures users receive notifications gradually over multiple days rather than being flooded on a single run.

The `SendWelcomeNotificationsWorker` uses the later of the feature's `welcome_notifications_live_at` setting and 8 days ago as its lower bound for user creation dates, so that the feature can be enabled retroactively without re-notifying users who joined long before the feature launched.

## Scenarios

### Bulk scheduling of welcome notifications

1. `Broadcasts::SendWelcomeNotificationsWorker` executes its `perform` method.
2. If `Settings::General.welcome_notifications_live_at` is not set, the worker exits immediately and no notifications are sent.
3. Otherwise, the worker computes a cutoff date as the maximum of `welcome_notifications_live_at` and 8 days ago.
4. The worker iterates over all users whose accounts were created after the cutoff date and calls `Broadcasts::WelcomeNotification::Generator` for each.

### Generator selects and enqueues one contextual notification

1. The generator loads the target user and checks whether the user's notification settings include `subscribed_to_welcome_notifications?`. If not, it exits without sending anything.
2. The generator evaluates six notification methods in order: welcome thread, authentication provider connection, feed customization, UX customization, discuss-and-ask, and app download.
3. For each method, it checks time-based eligibility (account age thresholds of 3 hours to 7 days), whether the corresponding notification has already been received, and any behavior-specific conditions (e.g., whether the user has commented in a welcome thread, is already authenticated with all providers, or follows enough tags).
4. The first method that passes all guards calls `Notification.send_welcome_notification` with the appropriate broadcast ID and sets `notification_enqueued` to `true`, stopping further evaluation for this run.

### Worker delivers a single welcome notification

1. `Notifications::WelcomeNotificationWorker` receives a `receiver_id` and a `broadcast_id`.
2. It looks up the broadcast in the set of active broadcasts. If the broadcast is not found or is inactive, the worker exits without creating a notification.
3. It calls `Notifications::WelcomeNotification::Send` with the receiver ID and the broadcast object.
4. The service builds a JSON payload containing the mascot account's user data and the broadcast's title, rendered HTML, and type, then creates a `Notification` record linked to the broadcast.
5. After creation, the service increments a `notifications.welcome` counter in Datadog tagged with the user ID and broadcast title.

### Discuss-and-ask notification is personalized to the user's activity

1. The generator determines whether the user has published articles tagged `explainlikeimfive` (asked a question) or `discuss` (started a discussion).
2. If the user has done only one of the two, the generator selects the complementary broadcast (encouraging the other activity).
3. If the user has done neither, the generator selects a generic discuss-and-ask broadcast.
4. If the user has done both, the notification is skipped entirely for this pass.

## Failures / Exceptions

- If `ActiveRecord::RecordNotFound` is raised while evaluating any notification method in the generator (e.g., because the expected active broadcast does not exist), the error is reported to Honeybadger and evaluation continues with the next method.
- Duplicate notifications are prevented at two levels: the generator checks `Notification.exists?` for the relevant broadcast before scheduling, and the `notification_enqueued` flag ensures at most one notification is sent per generator invocation.
