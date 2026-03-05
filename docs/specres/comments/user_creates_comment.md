---
id: "01KJ5DY1ASV3RY7Q7C930XDMBQ"
name: "user_creates_comment"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/comments_controller.rb`
- `app/services/comment_creator.rb`
- `app/models/comment.rb`
- `app/policies/comment_policy.rb`
- `spec/requests/comments_create_spec.rb` (Test)
- `spec/services/comment_creator_spec.rb` (Test)
- `spec/system/comments/user_fills_out_comment_spec.rb` (Test)
- `app/views/comments/new.html.erb` (Template)
- `app/views/comments/_form.html.erb` (Template)
- `app/javascript/packs/CommentTextArea/CommentTextArea.jsx`
- `app/javascript/packs/initializers/initializeCommentPreview.js`
- `app/javascript/packs/initializers/__tests__/initializeCommentPreview.test.js` (Test)

## Functional Overview

When a signed-in user submits a new comment on an article or another commentable resource, the system rate-limits the request based on how new the user's account is, builds a `Comment` record via `CommentCreator`, and authorizes the action through Pundit before checking whether the commenter has been blocked by anyone upstream in the thread. On successful save, the system automatically creates a "like" reaction from the author, subscribes them to all future replies via `NotificationSubscription`, dispatches new-comment notifications to relevant parties, and resolves any `@mention`s in the body. If the user has not yet agreed to the code of conduct, that flag is set on the user record at this point. Validation enforces a body length of 1–25,000 Markdown characters, uniqueness within the same parent thread, and that the target article is published and its discussion is not locked.

## Design Intent

`CommentCreator` is implemented as a `Delegator` subclass that wraps the underlying `Comment` record. This means callers can treat the `CommentCreator` instance as if it were the comment itself (policy authorization, attribute access) while keeping post-save side-effect logic — reactions, subscriptions, notifications, mentions — encapsulated inside the service. The separation prevents the controller from growing a long list of after-save callbacks and makes those side effects easy to stub in unit tests.

The rate-limit check uses two separate limits: a stricter `comment_antispam_creation` limit for accounts considered "new" by the platform, and a standard `comment_creation` limit for established users. This graduated approach reduces spam from newly registered accounts without penalizing regular contributors.

## Key Members

- `CommentCreator#save` — persists the record and, only if that succeeds, runs all post-save side effects; returns the creator instance (truthy) on success
- `Comment::BODY_MARKDOWN_SIZE_RANGE` — `1..25_000` characters; enforced by model validation
- `comment_antispam_creation` / `comment_creation` — the two rate-limit action keys chosen by whether the user `considered_new?`
- `UserBlock.blocking?(blocker_id, blocked_id)` — used by `permit_commenter` to detect block relationships between the commenter and the article author, parent-comment author, or any ancestor in the thread

## Scenarios

### Successful top-level comment

1. A signed-in user submits a comment body and the target article's identifier to `POST /comments`.
2. The system applies the appropriate rate limit (antispam for new accounts, standard for established users) and raises `RateLimitChecker::LimitReached` if exceeded.
3. `CommentCreator` builds and saves the `Comment` record; Pundit confirms the user is neither spam-flagged nor comment-suspended.
4. After a successful save, the system creates a "like" reaction on behalf of the author, creates a `NotificationSubscription` for the new comment, sends new-comment notifications, and resolves any `@mention`s in the body.
5. If the user had not previously accepted the code of conduct, that flag is now marked on their account.
6. The controller renders the newly created comment partial as JSON and returns HTTP 200.

### Reply to an existing comment

1. The user submits a comment with a `parent_id` referencing an existing comment.
2. If the parent comment is deeper than depth 2 and already has children, the system re-parents the new comment to the deepest descendant of the parent to keep thread depth manageable.
3. All post-save side effects (reaction, subscription, notifications, mentions) proceed identically to the top-level case.
4. The new comment appears nested under its designated parent in the thread.

### Blocked user attempt

1. The user submits a comment on an article or as a reply to a comment.
2. Before saving, `permit_commenter` checks whether the user is blocked by the article's author, by the direct parent comment's author, or by any ancestor in the upthread chain.
3. If any blocking relationship is found, the controller raises `ModerationUnauthorizedError` and returns HTTP 422 with the message "Not allowed due to moderation action".
4. No comment record is created and no side effects are triggered.

### Rate limit reached

1. The user submits a comment but has already reached their allowed creation rate within the current window.
2. The system raises `RateLimitChecker::LimitReached` before any record is built or saved.
3. The controller returns HTTP 429 Too Many Requests.

### Discussion locked or article unpublished

1. The user submits a comment on an article whose discussion is locked or that is not yet published.
2. Model validation fires `discussion_not_locked` or `published_article` and adds an error to the comment.
3. The comment fails to save; the controller returns HTTP 422 with the validation error message.

## Failures / Exceptions

- **Spam or comment-suspended user** — `CommentPolicy#create?` returns false; Pundit raises `NotAuthorizedError`, controller returns HTTP 401 with a localized authorization error message.
- **Body too short or too long** — `body_markdown` length falls outside `1..25_000`; model validation fails, controller returns HTTP 422.
- **Duplicate comment in same thread** — `body_markdown` uniqueness constraint fires; if a duplicate record is found in the database, it is destroyed and HTTP 422 is returned.
- **Blocked by article author** — `ModerationUnauthorizedError` is raised by `permit_commenter`; HTTP 422 with "Not allowed due to moderation action".
- **Blocked upthread** — same as above, detected by walking ancestor comment IDs and checking `UserBlock`.
- **New-user antispam score** — comments from users registered within 48 hours that contain an HTTP link receive a score of -3; bodies that match `Settings::RateLimit` spam triggers receive a score of -5. These are applied synchronously before save via `synchronous_spam_score_check`.
- **Generic StandardError** — any unhandled error is caught, authorization is skipped, and HTTP 422 is returned with a localized error message.
