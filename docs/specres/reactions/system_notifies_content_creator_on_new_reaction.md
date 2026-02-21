---
id: "01KHZ59AQ4W3GQVDAC6H33R4FD"
name: "system_notifies_content_creator_on_new_reaction"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/services/notifications/reactions/reaction_data.rb`
- `app/services/notifications/reactions/send.rb`
- `app/views/notifications/_aggregated_reactions.html.erb`
- `spec/services/notifications/reactions/reaction_data_spec.rb` (Test)
- `spec/services/notifications/reactions/send_spec.rb` (Test)

## Functional Overview

When a public reaction (like or other category) is added to an article or comment, the system notifies the content's owner — a `User` or an `Organization` — by creating or updating a single aggregated `Notification` record. The notification bundles all sibling reactions on the same reactable into one entry, always reflecting the most recent reactor and the full list of unique reaction categories. If all sibling reactions are removed, the notification is deleted. The `Notifications::Reactions::ReactionData` value object carries the identity of the reactable across process boundaries (e.g. into background jobs), validating that the reactable type is `"Article"` or `"Comment"` and that numeric IDs are present before any processing begins.

## Design Intent

A single aggregated notification per reactable per receiver is used intentionally so that a burst of reactions does not flood the recipient's notification feed. The upsert strategy (falling back to `Notification.upsert` with a targeted unique index when the record is not yet persisted) guards against duplicate rows under concurrent job execution. The `read` flag is reset to `false` only when the aggregated sibling count grows, preventing already-read notifications from being surfaced again for duplicate saves.

## Key Members

- `ReactionData` — lightweight value object carrying `reactable_id`, `reactable_type`, `reactable_user_id`, and `reactable_subforem_id`; raises `DataError` on construction if validation fails
- `Notifications::Reactions::Send#call` — entry point; returns a `Response` struct with fields `action` (`:saved` or `:deleted`) and `notification_id`
- `reaction_siblings` — the set of public-category reactions on the same reactable, excluding reactions made by the reactable's own author, used to decide whether a notification should exist

## Scenarios

### New reaction creates a notification for the content author

1. A reactor submits a public-category reaction on an article or comment they did not author.
2. The system coerces the reaction data into a `ReactionData` value object, validating that the reactable type and IDs are present and valid.
3. The system queries all existing public-category sibling reactions on the same reactable, excluding any made by the content author.
4. Because at least one sibling reaction exists, the system creates (or initializes) a `Notification` record with `action: "Reaction"`, stamping `notified_at` and setting `read` to `false`.
5. The notification's `json_data` is populated with the most recent reactor's user data, the reactable's path and title, and an `aggregated_siblings` array covering all sibling reactions.
6. The system returns a `Response` with `action: :saved` and the notification's ID.

### Subsequent reactions aggregate into the existing notification

1. Additional reactors add public-category reactions to the same reactable.
2. The system finds the existing `Notification` record via `find_or_initialize_by`.
3. The `aggregated_siblings` list grows; because the new sibling count exceeds the previous count, `read` is reset to `false` so the owner sees the updated notification.
4. The notification's `json_data` is updated to reflect the newest reactor and the full sibling list.
5. The system returns `action: :saved`.

### Last reaction is removed and the notification is deleted

1. A reactor removes their reaction, and no other public-category reactions remain on the reactable.
2. The system finds zero sibling reactions.
3. Any existing `Notification` record matching the reactable and receiver is deleted.
4. The system returns a `Response` with `action: :deleted`.

### A reaction is removed but sibling reactions remain

1. A reactor removes their reaction, but at least one sibling reaction from another user is still present.
2. The system rebuilds the notification using the remaining siblings as the new `aggregated_siblings`.
3. The existing notification is updated in place without changing the notification count.
4. The system returns `action: :saved`.

### Notification is sent to an organization receiver

1. An article owned by an organization receives a public reaction.
2. The system sets `organization_id` on the notification params instead of `user_id`.
3. A notification is created (or updated) associated with the organization rather than an individual user.

## Failures / Exceptions

- If the `ReactionData` value object is constructed with an invalid reactable type (not `"Article"` or `"Comment"`) or non-integer IDs, a `Notifications::Reactions::ReactionData::DataError` is raised immediately, before any notification logic runs.
- If the receiver is neither a `User` nor an `Organization`, `Notifications::Reactions::Send#call` returns `nil` without creating or modifying any notification.
- If an existing notification has unexpected or missing `json_data` (e.g. from legacy data), the previous sibling count defaults to `0` rather than raising an error.
