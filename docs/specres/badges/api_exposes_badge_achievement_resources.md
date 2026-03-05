---
id: "01KJ6FJA4XS9P5A266ZFW6Q7Y4"
name: "api_exposes_badge_achievement_resources"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/concerns/api/badge_achievements_controller.rb`
- `app/controllers/api/v0/badge_achievements_controller.rb`
- `app/controllers/api/v1/badge_achievements_controller.rb`
- `app/policies/badge_achievement_policy.rb`
- `spec/requests/api/v1/badge_achievements_spec.rb` (Test)

## Functional Overview

The API exposes CRUD operations for badge achievements via both the v0 and v1 API endpoints. The shared logic lives in a concern module that provides `index`, `show`, `create`, and `destroy` actions. Listing returns achievements paginated at 50 per page in descending creation order. Creating an achievement accepts `user_id`, `badge_id`, an optional custom context message, and a flag to include or suppress the default description. All endpoints are restricted to admin users, enforced through a Pundit policy that checks `any_admin?` on the authenticated user. The v0 variant authenticates via API key or session; v1 uses API key authentication exclusively.

## Design Intent

The behavior is implemented as a Rails concern mixed into separate v0 and v1 controllers so that authentication strategy and routing versioning can evolve independently without duplicating action logic. Authorization is delegated to Pundit's `BadgeAchievementPolicy#api?` to keep the access rule in a single, auditable location.

## Scenarios

### Admin lists all badge achievements

1. An admin sends `GET /api/badge_achievements` with a valid API key.
2. The system retrieves badge achievements ordered by creation date (newest first), limited to 50 per page.
3. The system returns HTTP 200 with the paginated JSON array.

### Admin retrieves a single badge achievement

1. An admin sends `GET /api/badge_achievements/:id` with a valid API key.
2. The system looks up the badge achievement by ID.
3. The system returns HTTP 200 with the achievement's JSON representation, including its `id`.

### Admin awards a badge to a user

1. An admin sends `POST /api/badge_achievements` with `user_id`, `badge_id`, an optional `rewarding_context_message_markdown`, and `include_default_description`.
2. The system creates a new `BadgeAchievement` record with the provided attributes.
3. The system returns HTTP 201 with the created achievement's JSON representation.

### Admin revokes a badge achievement

1. An admin sends `DELETE /api/badge_achievements/:id` with a valid API key.
2. The system locates the achievement by ID and destroys it.
3. The system returns HTTP 204 with no body.

## Failures / Exceptions

- If the new achievement fails model validation (e.g., awarding a non-repeatable badge to a user who already holds it), the system returns HTTP 422 with a JSON object containing an `errors` array of human-readable messages and does not persist the record.
