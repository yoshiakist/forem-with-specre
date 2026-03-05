---
id: "01KJ15S0NS9P24NVVX050NB1S1"
name: "system_notifies_user_on_badge_achievement"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/new_badge_achievement/send.rb`
- `app/workers/notifications/new_badge_achievement_worker.rb`
- `app/workers/badge_achievements/send_email_notification_worker.rb`
- `app/views/notifications/_badgeachievement.html.erb` (Template)
- `spec/services/notifications/new_badge_achievement/send_spec.rb` (Test)
- `spec/workers/notifications/new_badge_achievement_worker_spec.rb` (Test)
- `spec/workers/badge_achievements/send_email_notification_worker_spec.rb` (Test)

## Functional Overview

When a user earns a badge, the system delivers two asynchronous notifications via Sidekiq workers on the low-priority queue: an in-app notification record and a badge email. `Notifications::NewBadgeAchievementWorker` looks up the `BadgeAchievement` by ID and delegates to `Notifications::NewBadgeAchievement::Send`, which creates a `Notification` record linked to the user and the achievement, embedding badge details (title, image URL, credits awarded, and an optional description) as JSON. In parallel, `BadgeAchievements::SendEmailNotificationWorker` also looks up the achievement and delivers a `new_badge_email` via `NotifyMailer`. The in-app notification is rendered using a partial that displays the badge title, optional description, badge image, rewarding context message, a link to the user's profile, and a credit award notice when credits are granted.

## Design Intent

Both notification channels (in-app and email) run as separate low-priority workers so that badge award processing does not block the main request path. Each worker performs its own lookup and exits silently if the record no longer exists, making the jobs safe to retry without side effects.

## Key Members

- `badge_achievement` — the `BadgeAchievement` record carrying the earned badge, user reference, rewarding context message, and credit information
- `json_data` — serialized hash stored on the `Notification` record; includes user data, badge title, image URL, credits awarded, and conditionally the badge description
- `include_default_description` — flag on `BadgeAchievement` that controls whether the badge description is included in the notification payload

## Scenarios

### In-app notification created for a badge achievement

1. A `BadgeAchievement` record is created for a user who has earned a badge.
2. `Notifications::NewBadgeAchievementWorker` is enqueued with the achievement's ID.
3. The worker looks up the `BadgeAchievement` by ID and calls `Notifications::NewBadgeAchievement::Send`.
4. The service creates a `Notification` record associated with the user, with `notifiable_type` set to `"BadgeAchievement"` and `action` set to `nil`.
5. The notification's JSON payload contains user data, badge title, image URL, credits awarded, rewarding context message, and the badge description if `include_default_description` is true.

### In-app notification omits badge description when flag is false

1. A `BadgeAchievement` exists where `include_default_description` is false.
2. `Notifications::NewBadgeAchievement::Send` is called with that achievement.
3. The resulting `Notification` record's JSON payload contains a `nil` value for the badge description field.

### Badge email sent to user on achievement

1. `BadgeAchievements::SendEmailNotificationWorker` is enqueued with the achievement's ID.
2. The worker looks up the `BadgeAchievement` by ID.
3. The worker calls `NotifyMailer.with(badge_achievement:).new_badge_email.deliver_now` to send the badge email immediately.

### Worker does nothing when badge achievement record is not found

1. Either worker is enqueued with an ID that does not correspond to an existing `BadgeAchievement` (e.g., the record was deleted).
2. The lookup returns `nil`.
3. The worker exits without creating a notification or sending an email; no error is raised.

## Failures / Exceptions

- If `BadgeAchievement.find_by` returns `nil` (record not found or ID is `nil`), both workers exit silently without performing any action, allowing Sidekiq retries to be harmless.
