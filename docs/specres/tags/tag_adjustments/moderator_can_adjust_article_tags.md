---
id: "01KJ3ZG8Z0CF01S5WC6MP62WS6"
name: "moderator_can_adjust_article_tags"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/tag_adjustments_controller.rb`
- `app/models/tag_adjustment.rb`
- `app/services/tag_adjustment_creation_service.rb`
- `app/services/tag_adjustment_update_service.rb`
- `spec/requests/tag_adjustments_spec.rb` (Test)
- `spec/models/tag_adjustment_spec.rb` (Test)
- `spec/services/tag_adjustment_creation_service_spec.rb` (Test)
- `spec/services/tag_adjustment_update_service_spec.rb` (Test)
- `spec/factories/tag_adjustments.rb` (Test)

## Functional Overview

Moderators with appropriate privileges (tag moderators for the specific tag, admins, or super moderators) can add or remove tags on articles through the tag adjustment system. When a moderator submits a tag adjustment, `TagAdjustmentCreationService` validates the actor's permissions, resolves the tag record, persists a `TagAdjustment` record with status `committed`, updates the article's tag list accordingly, and dispatches a notification to the article author. Moderators can also revoke a previous adjustment via the destroy action, which deletes the record and reverses the tag change on the article — restoring a removed tag or removing an added one. The `TagAdjustmentUpdateService` provides a lower-level update path (currently incomplete) for mutating a tag adjustment's attributes such as status. All moderation actions are written to the audit log.

## Design Intent

The `adjustment_type` field (`"removal"` or `"addition"`) drives both the direction of the tag change and its reversal logic, making it possible to undo any adjustment deterministically without storing a separate before-state. Permission checking is enforced at two levels — the Pundit policy gate in the controller and a model-level validation — so that even programmatic `TagAdjustment` creation respects role boundaries.

## Key Members

- `adjustment_type`: `"removal"` or `"addition"` — determines whether the tag is removed from or added to the article
- `status`: one of `"committed"`, `"pending"`, `"committed_and_resolvable"`, `"resolved"` — lifecycle state of the adjustment
- `tag_name`: the canonical tag name (case-normalized to match the `Tag` record)
- `reason_for_adjustment`: free-text explanation stored on the record

## Scenarios

### Moderator removes a tag from an article

1. A user with the `tag_moderator` role for the target tag (or any admin / super moderator) submits `POST /tag_adjustments` with `adjustment_type: "removal"` and the target article id.
2. The controller authorizes the request via the `moderation_routes?` policy.
3. `TagAdjustmentCreationService` resolves the tag from the article's existing tag list (case-insensitive match) and builds a `TagAdjustment` record.
4. The model validates that the actor has privilege and that the tag is actually present on the article; if validation passes, the record is saved with status `"committed"`.
5. The service removes the tag from the article's tag list and sends a `Notification` to the article author.
6. For JSON requests the controller responds with `{ status: "Success", result: "removal", colors: { bg: ..., text: ... } }`; for HTML requests it redirects to the article's mod page.

### Moderator adds a tag to an article

1. A privileged moderator submits `POST /tag_adjustments` with `adjustment_type: "addition"` and the tag name to add.
2. Authorization and service initialization proceed identically to the removal flow.
3. `TagAdjustmentCreationService` looks up the `Tag` record by name and builds the `TagAdjustment`.
4. The model validates that the article does not already have 4 or more tags; if valid, the record is saved with status `"committed"`.
5. The service appends the tag to the article's tag list and notifies the author.
6. The controller responds or redirects in the same way as the removal success path.

### Validation failure on tag adjustment creation

1. A moderator submits a tag adjustment that fails model validation (e.g., adding to an article that already has 4 tags, removing a tag not present on the article, or acting on a tag for which the user lacks the moderator role).
2. The save fails and the controller re-authorizes the request.
3. For JSON requests the controller returns `{ error: <localized message with full error sentences> }`; for HTML requests it re-renders the `moderations/mod` template with the error state and the existing adjustments for the article.

### Moderator revokes a previous tag adjustment

1. A privileged moderator submits `DELETE /tag_adjustments/:id`.
2. The controller authorizes the request and finds the `TagAdjustment` by id.
3. The record is destroyed.
4. If the original adjustment was a `"removal"`, the tag is added back to the article's tag list; if it was an `"addition"`, the tag is removed from the article's tag list.
5. For JSON requests the controller responds with `{ result: <localized "destroyed" message> }`; for HTML requests it redirects to the article's mod page.

### Tag adjustment status update (partial)

1. `TagAdjustmentUpdateService` is initialized with an existing `TagAdjustment` record and a hash of updated attributes (e.g., `status: "resolved"`).
2. Calling `update` applies the attribute changes directly to the record via `update`.
3. No notification logic is triggered (notification update support is explicitly deferred).

## Failures / Exceptions

- Attempting to remove a tag that is not on the article's tag list raises a model validation error (`tag_id` — tag is not live on the article).
- Attempting to add a tag when the article already has 4 or more tags raises a model validation error (`base` — too many tags).
- Attempting to create a tag adjustment without the required moderator role for the given tag raises a model validation error (`user_id` — unpermitted).
- All moderation controller actions (create and destroy) emit an audit log entry via `Audit::Logger` as an after-action callback.
