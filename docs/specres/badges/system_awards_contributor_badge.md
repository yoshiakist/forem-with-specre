---
id: "01KJ6FRX20G8Y8FWD3TSEKZQPP"
name: "system_awards_contributor_badge"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/badges/award_contributor.rb`
- `spec/services/badges/award_contributor_spec.rb` (Test)

## Functional Overview

The `Badges::AwardContributor` service awards the "dev-contributor" badge to one or more users identified by their usernames. It accepts a list of usernames and an optional message (defaulting to a localized thank-you string), then delegates to the general `Badges::Award` service to create badge achievements for all matching users in a single call.

## Key Members

- `BADGE_SLUG` — The fixed badge slug `"dev-contributor"` that identifies which badge to award.
- `usernames` — A list of one or more usernames identifying the recipients.
- `message_markdown` — Optional Markdown-formatted message delivered alongside the badge; defaults to the localized `services.badges.thank_you` translation.

## Scenarios

### Award the contributor badge to a list of users

1. The caller provides a list of one or more usernames.
2. The system looks up all users whose usernames match the provided list.
3. The system invokes `Badges::Award` with those users, the `"dev-contributor"` slug, and the message.
4. A badge achievement is created for each matched user.

### Award the contributor badge with a custom message

1. The caller provides a list of usernames and a custom Markdown message string.
2. The system looks up all matching users.
3. The system invokes `Badges::Award` with the custom message instead of the default.
4. Each matched user receives a badge achievement containing the custom message.

### Award with default thank-you message when no message is supplied

1. The caller provides only a list of usernames, omitting the message argument.
2. The system uses the localized `services.badges.thank_you` string as the message.
3. The system looks up all matching users and delegates to `Badges::Award`.
4. Each matched user receives a badge achievement with the default thank-you message.
