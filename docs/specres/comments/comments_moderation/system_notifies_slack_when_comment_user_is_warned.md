---
id: "01KJ43EGBJ705B1E5KETFD0NYE"
name: "system_notifies_slack_when_comment_user_is_warned"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/slack/messengers/comment_user_warned.rb`
- `spec/services/slack/messengers/comment_user_warned_spec.rb` (Test)

## Functional Overview

When a comment is posted by a user who has been given the "warned" role, the system sends a Slack notification to the `warned-user-comments` channel. The notification includes a link to the comment, a truncated excerpt of the comment body, the commenter's username, and an internal admin link for managing the user. If the commenter has not been warned, no notification is sent. The message is dispatched asynchronously via `Slack::Messengers::Worker`.

## Design Intent

The early-return guard on the warned status keeps the messenger side-effect-free for non-warned users, avoiding unnecessary Slack noise. Routing the notification to a dedicated channel (`warned-user-comments`) and using the `sloan_watch_bot` identity allows moderators to monitor warned-user activity in one place without additional filtering.

## Key Members

- `comment` — the comment being evaluated; its author and body are the source of notification content
- `user` — the author of the comment, checked for the `warned` role before any notification is sent
- `MESSAGE_TEMPLATE` — a frozen format string that composes the activity URL, truncated comment text, username, and internal admin URL into the Slack message body

## Scenarios

### Comment posted by a non-warned user

1. `Slack::Messengers::CommentUserWarned` is called with a comment whose author does not hold the `warned` role.
2. The system checks whether the user is warned and finds they are not.
3. No Slack job is enqueued; the call exits immediately without side effects.

### Comment posted by a warned user

1. `Slack::Messengers::CommentUserWarned` is called with a comment whose author holds the `warned` role.
2. The system verifies the user is warned.
3. It constructs the Slack message using the comment's URL, the first 300 characters of the comment body, the commenter's username, and the admin URL for the user.
4. A job is enqueued via `Slack::Messengers::Worker` targeting the `warned-user-comments` channel, sent as `sloan_watch_bot` with the `:sloan:` emoji.
5. Slack receives the notification asynchronously.
