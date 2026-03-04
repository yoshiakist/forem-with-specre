---
id: "01KHZ55S8Z1A16PNGY9X7PR58P"
name: "admin_can_manage_flagged_reaction_status"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/reactions_controller.rb`
- `app/views/admin/shared/_flag_reactions_table.html.erb` (Template)
- `app/views/admin/shared/_flag_reaction_item.html.erb` (Template)
- `app/views/admin/shared/_flag_reaction_item_dropdown_menu.html.erb` (Template)
- `app/javascript/packs/admin/shared/flagReactionItemDropdownButton.js`
- `app/services/users/confirm_flag_reactions.rb`
- `app/workers/users/confirm_flag_reactions_worker.rb`
- `spec/requests/admin/reactions_spec.rb` (Test)
- `spec/services/users/confirm_flag_reactions_spec.rb` (Test)
- `spec/workers/users/confirm_flag_reactions_worker_spec.rb` (Test)

## Functional Overview

Admins can update the status of individual flagged (vomit-category) reactions through the admin panel. When an admin sets a reaction's status to `confirmed` or `invalid`, the change is persisted and the reacted-upon content's timestamp is refreshed. If the flagged target is a user profile and the new status is `confirmed`, the system additionally sinks the associated articles via `Moderator::SinkArticles`. For bulk confirmation of all flag reactions targeting a specific user and their content (articles and comments), the `Users::ConfirmFlagReactions` service is invoked — either directly or asynchronously through `Users::ConfirmFlagReactionsWorker` — which bulk-updates all `valid` vomit reactions on that user, their articles, and their comments to `confirmed`. Every status update performed by an admin is recorded to the audit log.

## Design Intent

The two-layer design — a per-reaction HTTP endpoint for granular admin decisions and a bulk-confirmation service invoked asynchronously for user-wide moderation actions — allows moderators to act on individual signals while also supporting efficient bulk remediation when a user is fully confirmed as a bad actor. The worker's `lock: :until_executing` option prevents duplicate enqueues from running concurrently.

## Key Members

- `status` (Reaction attribute) — allowed enum values include `valid`, `confirmed`, and `invalid`; only valid enum values are accepted by the model
- `Users::ConfirmFlagReactions` — service that bulk-confirms all live vomit reactions targeting a user, their articles, and their comments
- `Users::ConfirmFlagReactionsWorker` — Sidekiq job wrapping `Users::ConfirmFlagReactions`, queued at `medium_priority` with up to 10 retries

## Scenarios

### Admin confirms a flagged reaction

1. An authenticated admin sends `PUT /admin/reactions/:id` with `status: "confirmed"`.
2. The system finds the reaction and updates its status to `confirmed`.
3. The reactable content's `updated_at` timestamp is touched.
4. If the reaction targets a user profile and the category is `vomit`, `Moderator::SinkArticles` is called for that user.
5. The action is recorded in the audit log.
6. The system responds with HTTP 200 and `{ "outcome": "Success" }`.

### Admin invalidates a flagged reaction

1. An authenticated admin sends `PUT /admin/reactions/:id` with `status: "invalid"`.
2. The system finds the reaction and updates its status to `invalid`.
3. The reactable content's `updated_at` timestamp is touched.
4. The audit log records the action.
5. The system responds with HTTP 200 and `{ "outcome": "Success" }`.

### Admin submits an unrecognized status value

1. An authenticated admin sends `PUT /admin/reactions/:id` with a status value not recognized by the model (e.g., `"confirmedsssss"`).
2. The model validation fails; the status is not changed.
3. The system responds with HTTP 422 and a JSON body containing an `"error"` key describing the validation failure.

### Non-admin user attempts to update a reaction

1. A signed-in non-admin user sends `PUT /admin/reactions/:id`.
2. The system raises `Pundit::NotAuthorizedError`; the update is rejected.

### Bulk confirmation of flag reactions for a user

1. `Users::ConfirmFlagReactionsWorker` is enqueued with a user ID (or `Users::ConfirmFlagReactions` is called directly).
2. The worker looks up the user; if the user does not exist, execution stops silently.
3. `Users::ConfirmFlagReactions` queries all `vomit`-category reactions with status `valid` that target live reactable content.
4. It updates to `confirmed` all such reactions targeting the user's profile, the user's articles, and the user's comments in bulk.
5. Reactions targeting other users or non-vomit category reactions are left unchanged.

## Failures / Exceptions

- If the reaction record is not found, Rails raises `ActiveRecord::RecordNotFound` (standard 404 behavior).
- If the status value is not a valid enum member, the model returns an error message and the controller responds with HTTP 422.
- If the user ID passed to `Users::ConfirmFlagReactionsWorker` does not correspond to an existing user, the worker exits early without error.
