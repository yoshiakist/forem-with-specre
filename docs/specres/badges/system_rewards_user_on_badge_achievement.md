---
id: "01KJ6FWPJPKHJ0DPDHTN5AESN1"
name: "system_rewards_user_on_badge_achievement"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/badge_achievement.rb`
- `spec/models/badge_achievement_spec.rb` (Test)
- `spec/models/badge_reputation_bonus_spec.rb` (Test)

## Functional Overview

When a `BadgeAchievement` record is created, the system triggers several reward-oriented side effects before and after saving. Before validation, any Markdown in `rewarding_context_message_markdown` is rendered to sanitized HTML and stored in `rewarding_context_message`. After creation, the system awards credits to the recipient if the badge carries a non-zero `credits_awarded` value, and — exclusively for the "top-7" badge — doubles the recipient's `reputation_modifier` (capped at 4.0) and applies a 1.5x multiplier to all users who positively reacted to the recipient's articles within the past week (also capped at 4.0). A uniqueness validation prevents the same badge from being awarded to the same user more than once when the badge does not allow multiple awards. Notification delivery (in-app and email) is handled separately by the `system_notifies_user_on_badge_achievement` specre (ULID: 01KJ15S0NS9P24NVVX050NB1S1).

## Key Members

- `rewarding_context_message_markdown` — raw Markdown string provided by the rewarder; rendered to HTML before save
- `rewarding_context_message` — sanitized HTML output stored on the record after rendering
- `badge.credits_awarded` — integer number of credits the badge grants; zero means no credits are awarded
- `badge.allow_multiple_awards` — boolean controlling whether the same badge can be granted to a user more than once
- `user.reputation_modifier` — floating-point multiplier applied to the user's content scoring; capped at 4.0
- `badge_slug` — delegated slug from the associated badge; used to identify the "top-7" badge for special reputation logic

## Scenarios

### Credit awarding on badge achievement

1. A badge achievement is created for a user whose badge has a positive `credits_awarded` value.
2. After the record is persisted, the system adds the specified number of credits directly to the recipient's account.
3. If the badge's `credits_awarded` is zero, no credits are created and the user's credit balance is unchanged.

### Reputation modifier boost for Top 7 badge recipient

1. A badge achievement is created for a badge whose slug is "top-7".
2. After creation, the system doubles the recipient's current `reputation_modifier`.
3. If the doubled value would exceed 4.0, the modifier is capped at 4.0.
4. The system then locates all users who positively reacted (e.g., "like", "unicorn", "fire") to any of the recipient's articles published within the past week.
5. Each such user's `reputation_modifier` is multiplied by 1.5, again capped at 4.0.
6. The system logs the recipient's username and the count of updated positive reactors.

### Reputation logic is skipped for non-Top 7 badges

1. A badge achievement is created for any badge whose slug is not "top-7".
2. The system does not alter the recipient's `reputation_modifier` or any reactor's modifier.
3. No reputation-related log entries are written.

### Markdown rendering of rewarding context message

1. The rewarder supplies a Markdown string in `rewarding_context_message_markdown` when creating the achievement.
2. Before the record is validated, the system parses the Markdown and produces HTML.
3. The HTML is sanitized to permit only the tags and attributes allowed for badge achievement context messages.
4. The sanitized HTML is stored in `rewarding_context_message` on the record.

### Single-award badge uniqueness enforcement

1. A badge achievement is submitted for a user and a badge that does not permit multiple awards (`allow_multiple_awards` is false).
2. If the user already holds that badge, validation fails with a uniqueness error on `badge_id` scoped to `user_id`.
3. If the badge permits multiple awards, no uniqueness check is applied and the achievement is saved normally.

## Failures / Exceptions

- **Zero credits:** When `badge.credits_awarded` is zero, the credit-awarding step exits immediately without creating any credit records.
- **Non-Top 7 badge:** The reputation modifier block is guarded by a slug check; badges other than "top-7" skip all reputation calculations and logging.
- **Reputation modifier already at maximum:** If the recipient's or a reactor's `reputation_modifier` is already 4.0, the `[value, 4.0].min` guard prevents any change.
- **No positive reactions in time window:** If no users reacted positively to the recipient's recent articles, the reactor update loop runs zero iterations; the recipient's own modifier is still doubled.
- **User has no recent articles:** The article query returns an empty set; no reactors are found and only the recipient's modifier is updated.
- **No `rewarding_context_message_markdown`:** If the field is blank, the rendering callback returns early and `rewarding_context_message` is left unchanged.
- **Duplicate badge (single-award):** Attempting to award the same non-multiple-award badge twice to one user raises a validation error and the record is not saved.
