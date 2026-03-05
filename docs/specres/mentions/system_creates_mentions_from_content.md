---
id: "01KJ1ARF08DVRQE65SWASWAFWJ"
name: "system_creates_mentions_from_content"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/models/mention.rb`
- `app/services/mentions/create_all.rb`
- `app/workers/mentions/create_all_worker.rb`
- `app/decorators/mention_decorator.rb`
- `app/services/articles/updater.rb`
- `app/services/comment_creator.rb`
- `app/controllers/comments_controller.rb`
- `spec/models/mention_spec.rb` (Test)
- `spec/services/mentions/create_all_spec.rb` (Test)
- `spec/workers/mentions/create_all_worker_spec.rb` (Test)
- `spec/decorators/mention_decorator_spec.rb` (Test)
- `spec/factories/mentions.rb` (Test)

## Functional Overview

When a comment is created or updated, or when a published article is updated, the system parses the content's processed HTML to extract `@username` mentions embedded as `.mentioned-user` CSS-class links. It resolves those usernames against registered users, excludes the content author from being self-mentioned, and reconciles the resulting set with any pre-existing `Mention` records: stale mentions (whose usernames were removed from the text) are destroyed along with their associated notifications, while new mentions are created and paired with in-app notifications. For articles the notification is sent synchronously; for comments it is dispatched as a background job. After each `Mention` record is persisted, an email notification is enqueued if the mentioned user has email mention notifications enabled. Mentions embedded inside liquid tags or inline code snippets are intentionally excluded from detection.

## Design Intent

Article mention notifications are created synchronously so that the mention record exists in the database before any other article-level notifications are processed. Comment mention notifications are deferred to a background job because comments do not have the same ordering dependency and deferral reduces response latency. The worker guards against processing anything other than `Comment` notifiables, since article mentions are handled inline by `Mentions::CreateAll` called directly from `Articles::Updater`.

## Key Members

- `Mention` — polymorphic record linking a `user` to a `mentionable` (Article or Comment); unique per user-mentionable pair
- `Mentions::CreateAll` — service object that orchestrates extraction, reconciliation, and creation of mentions for a given notifiable
- `Mentions::CreateAllWorker` — Sidekiq job (default queue, 10 retries) that invokes `Mentions::CreateAll` asynchronously for comments
- `MentionDecorator#formatted_mentionable_type` — returns `"post"` for articles, or the downcased type string for other mentionable types
- `MentionDecorator#mentioned_by_blocked_user?` — returns true when the mentionable type is `"User"` and the mentioner has been blocked by the mentioned user

## Scenarios

### New comment is created with @mentions

1. A user submits a new comment containing one or more `@username` references.
2. `CommentCreator` saves the comment, then calls `Mention.create_all` which enqueues a `Mentions::CreateAllWorker` job.
3. The worker finds the `Comment` record and calls `Mentions::CreateAll`.
4. The service parses the processed HTML, collects the matching registered users (excluding the comment author), and creates a `Mention` record for each.
5. A background mention notification is dispatched for each new mention, and an email notification job is enqueued for users with email mentions enabled.

### Comment is edited and @mentions change

1. A user updates a comment, adding or removing `@username` references.
2. The `CommentsController#update` action calls `Mention.create_all` after saving, enqueuing a `Mentions::CreateAllWorker` job.
3. The worker calls `Mentions::CreateAll`, which re-parses the processed HTML and computes the current set of mentioned users.
4. Mentions for users no longer present in the text are destroyed, and their associated notifications are removed.
5. New `Mention` records are created for newly added users, with notifications dispatched accordingly.

### Published article is updated with @mentions

1. An editor updates a published article through `Articles::Updater`.
2. If the article remains published, `Mentions::CreateAll` is called directly (not via a worker).
3. The service extracts mentioned usernames from the article's processed HTML, excluding liquid-tag-embedded mentions and inline code snippets.
4. Mentions no longer in the text are destroyed and their notifications removed; new mentions are created with synchronous notifications so that mention records exist before other article notifications are issued.

### Mention inside liquid tag or code snippet is ignored

1. Content contains an `@username` that appears inside a liquid tag block (e.g., an embedded comment liquid tag) or within a backtick code snippet.
2. When `Mentions::CreateAll` parses the processed HTML, it rejects `.mentioned-user` links that are descendants of `.liquid-comment` or any element whose class begins with or contains `ltag`.
3. No `Mention` record is created for the embedded reference; the targeted user receives no notification.

### Author self-mention is silently skipped

1. A content author includes their own `@username` in the body of an article or comment they own.
2. `Mentions::CreateAll` filters out any user whose ID matches the notifiable's `user_id`.
3. No `Mention` record is created for the author, and no notification is sent.

## Failures / Exceptions

- A `Mention` is rejected if the mentionable record itself is invalid (e.g., a comment with no commentable); the `permission` validation adds an error and the record is not persisted.
- A user-mentionable pair must be unique; attempting to create a duplicate `Mention` fails validation and the duplicate is not persisted.
- If the notifiable record is not found by the worker (e.g., deleted before the job runs), `Mentions::CreateAll` is not called and the job exits silently.
- If a user who is mentioned in a comment already has a comment-level notification for that comment, no additional mention notification is created for them.
