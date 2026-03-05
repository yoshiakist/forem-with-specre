---
id: "01KHZ6M3H0WPQNH4GKB6YPAR1T"
name: "system_moderates_profile_content"
status: "draft"
---

## Related Files

- `app/workers/users/handle_profile_spam_worker.rb`
- `app/services/ai/profile_moderation_labeler.rb`

## Functional Overview

When a user's profile is updated, the system enqueues a background job (`Users::HandleProfileSpamWorker`) that delegates to `Spam::Handler` to evaluate the profile for spam. As part of that evaluation, `Ai::ProfileModerationLabeler` sends the user's profile data and up to two recent published articles to an AI client, which returns a single moderation label from a fixed vocabulary. The label classifies the profile on a spectrum from clearly acceptable content to clear and obvious spam, harmful content, or incitement. If the AI call fails, the labeler defaults to `no_moderation_label` so that transient errors do not block the user.

## Design Intent

The AI labeler is intentionally conservative: its guidelines instruct the model to prefer `no_moderation_label` for borderline or legitimate-looking content and to act only on clear and obvious violations. This minimises false positives while still catching unmistakable spam and abuse without requiring human review for every profile update.

## Key Members

- `LABELS` — ordered list of 14 moderation label strings that the AI must choose from; the labeler validates the response against this list and falls back to `no_moderation_label` if the response cannot be matched.
- `community_description` — community context fetched from `Settings::RateLimit.internal_content_description_spec` (or `Settings::Community.community_description`) for the default subforem; included in the AI prompt so labeling is relative to the community's purpose.

## Scenarios

### Profile update triggers spam check

1. A user's profile is updated and `Users::HandleProfileSpamWorker` is enqueued with the user's ID.
2. The worker looks up the user; if the user no longer exists it exits early without error.
3. The worker calls `Spam::Handler.handle_profile_update!` with the user object, which orchestrates the full moderation flow including invoking `Ai::ProfileModerationLabeler`.

### AI labels a profile as clear spam

1. `Ai::ProfileModerationLabeler` is initialized with the user.
2. The labeler assembles a prompt containing the community description, profile fields (name, username, summary, website URL, location, article count, comment count), and the body of up to two recent published articles (each truncated to 1,200 characters).
3. The prompt instructs the AI to return exactly one label from `LABELS`.
4. The AI responds with `clear_and_obvious_spam`; the labeler matches it against `LABELS` and returns it to the caller.

### AI labels a borderline or legitimate profile

1. The prompt is assembled as above.
2. The AI evaluates the profile and finds no clear violation; it responds with `okay_and_on_topic` or another non-spam label.
3. The labeler matches the response against `LABELS` and returns the matched label.

### User has no published articles

1. The labeler builds the prompt but the user has no published articles.
2. The articles section of the prompt is replaced with "No published articles available."
3. The AI evaluates the profile-only context and returns a label; the labeler returns it to the caller.

### AI call fails

1. The AI client raises a `StandardError` during the call.
2. The labeler rescues the exception, logs an error message, and returns `no_moderation_label`.
3. The profile update is not blocked; moderation proceeds as if no label was assigned.

## Failures / Exceptions

- If `User.find_by(id: user_id)` returns nil the worker returns immediately, preventing errors for already-deleted users.
- If the AI response is blank or does not contain any known label string, the labeler returns `no_moderation_label` as the safe default.
- Any `StandardError` raised by the AI client is caught, logged via `Rails.logger.error`, and resolved to `no_moderation_label`.
