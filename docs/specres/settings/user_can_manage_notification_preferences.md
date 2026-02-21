---
id: "01KHZ454YXRB8TWV8PC06P4EQ5"
name: "user_can_manage_notification_preferences"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/users/notification_settings_controller.rb`
- `spec/requests/user/user_notification_settings_spec.rb` (Test)
- `spec/factories/users_notification_settings.rb` (Test)

## Functional Overview

An authenticated user can manage their notification preferences through the Notifications tab of the settings page. The controller updates the user's `Users::NotificationSetting` record with toggles for various email and mobile notification types. After saving, the system syncs email eligibility and triggers Mailchimp newsletter subscription updates when the newsletter preference changes. The controller supports both a full parameter set for the settings page and a limited `ONBOARDING_ALLOWED_PARAMS` set for the onboarding flow. Suspended users are blocked from accessing this feature.

## Key Members

- `ALLOWED_PARAMS` — full set of toggleable notification types: email (badge, comment, community mod newsletter, digest, follower, membership newsletter, mention, newsletter, tag mod newsletter, unread), mobile (comment, mention), and other (mod roundrobin, reaction, welcome)
- `ONBOARDING_ALLOWED_PARAMS` — limited subset for onboarding flow

## Scenarios

### User toggles email notification preferences

1. Authenticated user navigates to the Notifications tab in settings
2. User enables or disables individual email notification types (badges, comments, followers, mentions, digest, unread notifications)
3. System updates the user's `Users::NotificationSetting` record
4. User is redirected back to the Notifications tab

### User toggles mobile notification preferences

1. User enables or disables mobile notifications for comments and mentions
2. System persists the `mobile_comment_notifications` and `mobile_mention_notifications` settings

### User changes newsletter subscription

1. User toggles `email_newsletter` preference
2. System persists the change and triggers email eligibility sync
3. If the newsletter preference changed, system enqueues Mailchimp subscription update

### User updates notification preferences during onboarding

1. During onboarding flow, a limited set of notification parameters is available
2. System only permits `ONBOARDING_ALLOWED_PARAMS` when the onboarding context is active
3. Preferences are saved with the same persistence and sync logic

### User toggles moderator and reaction notifications

1. User enables or disables `reaction_notifications`, `mod_roundrobin_notifications`, and `welcome_notifications`
2. System persists the values; moderator notifications are only shown to trusted users

## Failures / Exceptions

- Suspended users are blocked by `check_suspended` before-action
- Errors during save are logged to Honeycomb for observability
