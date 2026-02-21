---
id: "01KHZ55SRCPDHPWM0EYSTE60MK"
name: "user_can_react_to_article"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/models/reaction.rb`
- `app/models/reaction_category.rb`
- `app/controllers/reactions_controller.rb`
- `app/javascript/packs/articleReactions.js`
- `app/javascript/actionsPanel/services/reactions.js`
- `app/views/articles/_multiple_reactions.html.erb`
- `app/javascript/articles/components/ReactionsCount.jsx`
- `app/workers/reactions/bust_reactable_cache_worker.rb`
- `app/workers/reactions/bust_homepage_cache_worker.rb`
- `app/workers/reactions/update_relevant_scores_worker.rb`
- `spec/models/reaction_spec.rb` (Test)
- `spec/models/reaction_category_spec.rb` (Test)
- `spec/requests/reactions_spec.rb` (Test)
- `spec/workers/reactions/bust_reactable_cache_worker_spec.rb` (Test)
- `spec/workers/reactions/bust_homepage_cache_worker_spec.rb` (Test)
- `spec/workers/reactions/update_relevant_scores_worker_spec.rb` (Test)
- `app/javascript/articles/components/__tests__/ReactionsCount.test.jsx` (Test)
- `spec/factories/reactions.rb` (Test)
- `spec/models/shared_examples/sync_reactions_count.rb` (Test)

## Functional Overview

Authenticated users can react to articles using one of several public reaction categories (such as `like`, `unicorn`, `raised_hands`, `fire`, and `exploding_head`) or save an article to their reading list via the `readinglist` category. Reactions are toggled via `POST /reactions`: creating the reaction on the first request and destroying it on a subsequent identical request. Negative and privileged categories (`thumbsdown`, `vomit`, `thumbsup`) are restricted to trusted users and moderators. After every create or destroy event, background workers bust edge-cache keys for the reactable (article or comment), conditionally bust the homepage cache when a featured article is affected, and update hotness scores and follower points to reflect the new reaction state. The article page loads reaction counts and the current user's reactions asynchronously via `GET /reactions?article_id=:id`, and the UI updates optimistically before the server confirms the change.

## Design Intent

The toggle-on-repeat-POST approach avoids a separate DELETE endpoint and keeps the client interaction uniform: one button, one endpoint. Optimistic UI toggling (immediately reflecting the change before the server responds) keeps the interface feeling responsive, with a rollback if the server returns an error. Cache-busting is handled asynchronously via high-priority Sidekiq jobs so the write path stays fast; the homepage cache is only busted when the reacted article is among the top three featured articles, limiting unnecessary cache churn.

## Key Members

- `category` — reaction type slug; public values are `like`, `unicorn`, `raised_hands`, `fire`, `exploding_head`; `readinglist` is public but treated separately; privileged values are `thumbsup`, `thumbsdown`, `vomit`
- `status` — lifecycle status of the reaction record: `valid`, `invalid`, `confirmed`, `archived`
- `points` — computed score weight assigned by `CalculateReactionPoints`; negative points suppress notifications
- `reactable_type` / `reactable_id` — polymorphic reference to `Article`, `Comment`, or `User`

## Scenarios

### User reacts to an article for the first time

1. The article page loads and the client calls `GET /reactions?article_id=:id` to fetch current reaction counts and the signed-in user's existing reactions.
2. The user clicks a reaction button in the reaction drawer.
3. The UI immediately toggles the button to the active state and increments the displayed count (optimistic update). The button is disabled during the request.
4. The client submits `POST /reactions` with `reactable_type=Article`, `reactable_id`, and `category`.
5. The server creates a `Reaction` record, assigns points, and returns `{ result: "create", category: "..." }`.
6. Cache keys for the article are invalidated; background workers update hotness scores and, if applicable, bust the homepage cache.
7. The button is re-enabled. The UI reflects the confirmed state.

### User un-reacts (toggles off an existing reaction)

1. The user clicks the same reaction button that is currently active.
2. The UI immediately toggles the button to the inactive state and decrements the count.
3. The client submits `POST /reactions` with the same parameters as before.
4. Because a matching reaction record already exists, `ReactionHandler.toggle` destroys it and returns `{ result: "destroy", category: "..." }`.
5. Cache keys are invalidated synchronously (before destroy) and scores are updated asynchronously.
6. The button is re-enabled.

### Unauthenticated user attempts to react

1. The user clicks a reaction button while not signed in.
2. The client detects the `logged-out` user status via `data-user-status` on the document body.
3. A login modal is shown immediately; no request is sent to `POST /reactions`.

### Trusted user applies a privileged reaction

1. A user with the `trusted` role clicks a moderation reaction (`thumbsup`, `thumbsdown`, or `vomit`).
2. The client submits `POST /reactions` with the privileged category.
3. `ReactionsController` delegates authorization to `ReactionPolicy`; a non-trusted user would receive a `Pundit::NotAuthorizedError`.
4. If the new reaction contradicts an existing one (e.g., `thumbsup` when `thumbsdown` is present), the contradictory reaction is removed atomically.
5. The reaction is created and background processing proceeds as in the standard flow.

### Reaction count display on article cards

1. An article card in a feed renders the `ReactionsCount` component, which receives `article.public_reactions_count` and `article.public_reaction_categories`.
2. If the count is zero the component renders nothing.
3. If the count is one or more, the component shows category icons (in descending count order) and the total count with appropriate singular or plural label.

## Failures / Exceptions

- Reacting on an unpublished article is rejected at the model validation layer with an error on `reactable_id`.
- A non-trusted user attempting a negative reaction category (`vomit`, `thumbsdown`) receives a model validation error, and a non-trusted user attempting `thumbsup` is rejected by the policy layer with `Pundit::NotAuthorizedError`.
- Exceeding the `reaction_creation` rate limit returns HTTP 429 before any reaction record is created.
- If the server returns a non-200 response, the client rolls back the optimistic UI toggle and displays an error modal.
- Background workers handle missing reaction records gracefully: if the record no longer exists, the worker returns early without raising an error.
