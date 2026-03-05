---
id: "01KJVS4H4SB05PGMMFNHGWXVV4"
name: "moderator_can_rate_article_quality"
status: "draft"
---

## Related Files

- `app/policies/rating_vote_policy.rb`
- `app/controllers/rating_votes_controller.rb`
- `spec/requests/rating_votes_spec.rb` (Test)

## Functional Overview

Moderators and trusted users can rate articles by submitting a quality vote through `POST /rating_votes`. The `RatingVotePolicy` gates access by requiring that the acting user is neither spam-flagged nor suspended. The controller upserts a `RatingVote` record (one per user per article) using the submitted rating value and group, logs the action to the moderator audit trail, and responds with a JSON success payload or an error message when the record fails to save.

## Scenarios

### Trusted user submits a rating vote

1. A trusted, non-suspended user sends a POST request to `/rating_votes` with an article ID, a numeric rating, and a group name.
2. The system authorizes the request via `RatingVotePolicy#create?`, confirming the user is not spam or suspended.
3. The system looks up an existing `RatingVote` for that user and article, or initializes a new one.
4. The vote is saved with the provided rating and group values.
5. The moderator action is recorded in the audit log.
6. The system responds with `{ result: "Success" }` (JSON) or redirects to `/mod` (HTML).

### Upsert — user updates an existing vote

1. A trusted user who has previously rated the same article submits a new rating.
2. The system finds the existing `RatingVote` record for that user-article pair instead of creating a new one.
3. The existing record is updated with the new rating and group values and saved.
4. The response is identical to a fresh creation.

### Non-trusted or spam/suspended user is denied

1. A user who is spam-flagged or suspended sends a POST request to `/rating_votes`.
2. `RatingVotePolicy#create?` returns `false` and Pundit raises `NotAuthorizedError`.
3. The request is rejected; no `RatingVote` record is created and nothing is written to the audit log for this request.

## Failures / Exceptions

- If `rating_vote.save` fails (e.g., validation errors), the system responds with a JSON error containing the full error message (HTTP 422) or renders an error result in HTML format.
