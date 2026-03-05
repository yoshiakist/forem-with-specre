---
id: "01KJ6FS1TBTFY751JJQTJ7F755"
name: "system_awards_fab_five_badge"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/badges/award_fab_five.rb`
- `spec/services/badges/award_fab_five_spec.rb` (Test)

## Functional Overview

The system awards the "Fab 5" badge to a given list of users identified by their usernames. When called, it delegates to the general `Badges::Award` service, passing the resolved user records, the fixed badge slug `"fab-5"`, and an optional congratulatory message. If no message is provided, a default one is generated using the community name from the site settings and the standard internationalization helper.

## Key Members

- `BADGE_SLUG` — the fixed identifier `"fab-5"` that targets the Fab 5 badge record.
- `usernames` — an array of username strings identifying the recipients.
- `message_markdown` — the body of the notification message delivered to each recipient; defaults to a localized congratulations string that includes the community name.

## Scenarios

### Award badge to one or more users with the default message

1. A caller supplies a list of one or more usernames.
2. The system looks up the corresponding user records by those usernames.
3. The system invokes the general badge-award service with the user records, the `"fab-5"` badge slug, and the default congratulatory message.
4. Each matching user receives a badge achievement record and a notification containing the congratulatory message.

### Award badge with a custom message

1. A caller supplies a list of usernames and an explicit Markdown message string.
2. The system looks up the corresponding user records by those usernames.
3. The system invokes the general badge-award service with the user records, the `"fab-5"` badge slug, and the caller-supplied message.
4. Each matching user receives the badge and a notification using the custom message instead of the default one.

### Default message uses the community name

1. When no message is provided, the system generates a congratulatory message by reading the community name from `Settings::Community.community_name`.
2. The message is formatted via the `services.badges.congrats` i18n key.
3. This ensures the notification text reflects the site's configured community identity.
