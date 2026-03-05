---
id: "01KJ6FSCYDY8QPVA6XPZ8X4WT1"
name: "system_awards_top_seven_badge"
status: "draft"
---

## Related Files

- `app/services/badges/award_top_seven.rb`
- `spec/services/badges/award_top_seven_spec.rb` (Test)

## Functional Overview

`Badges::AwardTopSeven` is a service object that grants the "top-7" badge to a given list of users. It accepts a list of usernames and an optional custom congratulatory message, looks up the corresponding `User` records, and delegates to `Badges::Award` to create the badge achievements. If no custom message is provided, a default message is generated from the community name via an i18n translation. Reputation modifier changes triggered by receiving the badge are handled automatically through the `BadgeAchievement` callback and are not the responsibility of this service.

## Scenarios

### Award the top-seven badge to a list of users

1. The caller provides a list of usernames identifying this week's top seven contributors.
2. The system looks up the corresponding user records.
3. The system invokes `Badges::Award` with the "top-7" badge slug, the user records, and the default congratulatory message.
4. A `BadgeAchievement` record is created for each user.

### Award the badge with a custom congratulatory message

1. The caller provides a list of usernames along with a custom message string.
2. The system looks up the corresponding user records.
3. The system invokes `Badges::Award` using the custom message instead of the default.
4. Each user receives the badge with the custom message attached.

### Generate the default congratulatory message

1. No custom message is supplied by the caller.
2. The system reads the community name from `Settings::Community`.
3. The system constructs the message using the `services.badges.congrats` i18n key and the community name.
4. This message is passed through to `Badges::Award`.
