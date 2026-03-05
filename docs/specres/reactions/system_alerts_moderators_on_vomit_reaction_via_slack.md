---
id: "01KJVD2BA0DGWK8HW05G0DHB9Z"
name: "system_alerts_moderators_on_vomit_reaction_via_slack"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/slack/messengers/reaction_vomit.rb`
- `spec/services/slack/messengers/reaction_vomit_spec.rb` (Test)

## Functional Overview

When a user reacts with a "vomit" reaction on any reactable content, the system dispatches an asynchronous Slack message to the `abuse-reports` channel. The message includes the reacting user's name, a link to their profile, and a link to the content they reacted on. This alert enables moderators to review potentially abusive or offensive content flagged by the community. Only vomit-category reactions trigger this notification; all other reaction categories are silently ignored.

## Design Intent

The vomit reaction is treated as a community abuse signal. By routing alerts to a dedicated `abuse-reports` channel via a named bot (`abuse_bot` with a crying emoji), moderators can triage flagged content without manual monitoring.

## Scenarios

### Vomit reaction triggers a Slack alert

1. A user places a reaction of category "vomit" on some reactable content.
2. The system formats a message containing the user's display name, a URL to the user's profile, and a URL to the reacted-on content.
3. The system enqueues an asynchronous Slack message to the `abuse-reports` channel, sent by the `abuse_bot` user with the `:cry:` emoji icon.

### Non-vomit reaction is ignored

1. A user places a reaction of any category other than "vomit" (e.g., "like").
2. The system takes no action; no Slack message is enqueued.

## Failures / Exceptions

- If the reaction's category is not `"vomit"`, the messenger returns immediately without sending any Slack notification.
