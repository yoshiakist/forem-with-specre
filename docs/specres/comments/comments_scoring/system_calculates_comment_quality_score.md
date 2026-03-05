---
id: "01KJ44CT90TACT5K15BYFV2H07"
name: "system_calculates_comment_quality_score"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/comments/calculate_score.rb`
- `app/workers/comments/calculate_score_worker.rb`
- `app/queries/comments/count.rb`
- `spec/services/comments/calculate_score_spec.rb` (Test)
- `spec/workers/comments/calculate_score_worker_spec.rb` (Test)
- `spec/queries/comments/count_spec.rb` (Test)

## Functional Overview

When a comment is created or updated, the system asynchronously calculates and persists a quality score for it. The `Comments::CalculateScoreWorker` Sidekiq job receives a comment ID, looks up the comment, and delegates to `Comments::CalculateScore`. That service retrieves a base quality score from `BlackBox`, then applies two adjustments: a 500-point penalty if the comment's author is flagged as a spammer, and a bonus equal to `Settings::UserExperience.index_minimum_score` if the author is a base subscriber. The final score is written directly to the database with `update_columns`. Afterward, timestamps are touched on both the comment's author and its commentable (when it supports `last_comment_at`). If the commentable is an `Article`, the article's displayed comment count is recalculated by `Comments::Count`, which excludes childless comments whose score falls below `Comment::HIDE_THRESHOLD`. Finally, the comment's cache (and transitively the commentable's cache) is busted via `Comments::BustCacheWorker`.

## Key Members

- `Comment::HIDE_THRESHOLD` — score threshold below which a childless comment is excluded from the displayed count
- `Settings::UserExperience.index_minimum_score` — bonus score added for base-subscriber authors
- `recalculate` flag on `Comments::Count` — when `true`, forces a fresh SQL count even if `displayed_comments_count` is already present on the article

## Scenarios

### Worker receives a valid comment ID and triggers scoring

1. A job is enqueued on the `medium_priority` queue with a comment ID.
2. The worker looks up the comment by ID.
3. The worker calls `Comments::CalculateScore` with the found comment.

### Worker receives an invalid or missing comment ID

1. A job is enqueued with a comment ID that does not exist in the database.
2. The worker looks up the comment and finds nothing.
3. The worker exits immediately without raising an error.

### System scores a comment from a regular user

1. The service receives a comment whose author is neither a spammer nor a base subscriber.
2. `BlackBox.comment_quality_score` returns a base score for the comment.
3. The base score is written to the comment record along with an updated `updated_at` timestamp.
4. The author's `last_comment_at` is touched, and the commentable's `last_comment_at` is touched if applicable.
5. If the commentable is an `Article`, the article's displayed comment count is recalculated and persisted.
6. The comment cache (and commentable cache) is busted.

### System applies a spam penalty to the score

1. The service receives a comment whose author is flagged as a spammer.
2. The base score from `BlackBox` is reduced by 500 points.
3. The penalised score is persisted to the comment record.

### System applies a subscriber bonus to the score

1. The service receives a comment whose author is a base subscriber.
2. The value of `Settings::UserExperience.index_minimum_score` is added to the base score from `BlackBox`.
3. The boosted score is persisted to the comment record.

### System recalculates an article's displayed comment count

1. `Comments::Count` is called for an article with `recalculate: true`, or when the article has no cached `displayed_comments_count`.
2. A SQL query counts all comments for the article that are below `Comment::HIDE_THRESHOLD` and have no child comments.
3. That hidden-comment count is subtracted from the total comment count to produce the displayed count.
4. The displayed count is saved to the article and returned.
5. When `recalculate: false` and a cached count already exists, the cached value is returned without running the SQL query.

## Failures / Exceptions

- If the comment ID passed to the worker does not match any record, the job returns early with no error, preventing spurious job failures from race conditions with deletions.
