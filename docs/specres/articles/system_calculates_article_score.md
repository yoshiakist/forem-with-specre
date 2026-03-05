---
id: "01KJBV19F8R23CVAD98DQATZ4G"
name: "system_calculates_article_score"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/models/article.rb`
- `app/lib/black_box.rb`
- `app/workers/articles/score_calc_worker.rb`
- `spec/models/article_spec.rb` (Test)
- `spec/workers/articles/score_calc_worker_spec.rb` (Test)

## Functional Overview

When an article is published, the system asynchronously enqueues a background job (`Articles::ScoreCalcWorker`) to recalculate that article's scores. The job calls `update_score` on the article, which computes three values and persists them atomically: a reaction-based `score` adjusted by spam status, user reputation signals, automod content moderation labels, badge bonuses, and an optional `max_score` cap; a `comment_score` summing each comment's score (clamped so no single comment contributes less than -1) also subject to the same cap; and a `hotness_score` produced by `BlackBox.article_hotness_score`, which blends time-based recency bonuses, a per-article epoch offset, reaction points (halved or quartered for older posts), a watercooler tag penalty, and a featured-article bonus.

## Design Intent

Score calculation is deliberately deferred to a background job so that publish-path latency is unaffected. The `lock: :until_executing` Sidekiq option prevents duplicate recalculations from stacking up. The `max_score` ceiling exists as a manual override to cap viral amplification for specific articles or users. `AUTOMOD_SCORE_ADJUSTMENTS` externalises the mapping from moderation labels to point deltas, making policy changes a constant edit rather than a logic change. `BlackBox.last_mile_hotness_calc` uses a custom epoch (2010-01-01) so that raw publish-time offsets are relative to the platform's founding rather than Unix epoch, keeping numbers human-readable.

## Key Members

- `AUTOMOD_SCORE_ADJUSTMENTS` — constant hash mapping each `automod_label` symbol to a signed integer point delta applied to `score`
- `max_score` — per-article ceiling; the lower of article `max_score` and user `max_score` is used; a value of 0 means no cap
- `score` — persisted aggregate reaction score including all adjustments
- `comment_score` — persisted sum of comment scores, each floored at -1, optionally capped
- `hotness_score` — persisted feed-ranking score computed by `BlackBox.article_hotness_score`
- `privileged_users_reaction_points_sum` — persisted sum of reactions in the privileged category, updated alongside score

## Scenarios

### Score calculation triggered on publish

1. An article transitions to published state.
2. `async_score_calc` is called; it verifies the article is published and not destroyed, then enqueues `Articles::ScoreCalcWorker` with the article's id.
3. The worker picks up the job, looks up the article by id, and calls `update_score`.

### Worker skips missing article

1. The worker receives an article id that no longer exists in the database.
2. The lookup returns nil and the worker returns early without raising an error or calling any scoring logic.

### Reaction score computed with adjustments

1. The system sums all reaction points on the article.
2. It applies signed adjustments for: spam user (-500), negative user reactions, base subscriber bonus, user featured-article count bonus (log-scaled), user negative-article count penalty (log-scaled), context note count, automod label delta from `AUTOMOD_SCORE_ADJUSTMENTS`, user badge bonus (square-root of badge weight sum), and organisation baseline score.
3. If the resulting score exceeds the effective `max_score` cap (minimum of article and user max, ignoring zero), the score is clamped to the cap.
4. The final `score`, `comment_score`, `hotness_score`, and `privileged_users_reaction_points_sum` are written to the database in a single `update_columns` call.

### Comment score computed with floor and cap

1. The system iterates all comments on the article, taking each comment's score but treating any value below -1 as -1.
2. These floored values are summed to produce `comment_score`.
3. If the effective `max_score` cap is positive and the sum exceeds it, `comment_score` is clamped to the cap.

### Hotness score blends recency, reactions, and epoch offset

1. `BlackBox.article_hotness_score` selects the article's `crossposted_at` date if available, otherwise `published_at`.
2. Time-based step bonuses are added for posts published within the last 1, 8, 12, 26, 48, and 96 hours.
3. Reaction points are halved for posts older than 4 days and quartered for posts older than 7 days.
4. Posts tagged "watercooler" receive an 80% reaction-point weight.
5. Featured articles receive an additional flat bonus.
6. `last_mile_hotness_calc` adds a base value derived from seconds since the custom epoch divided by 1000, plus capped contributions from `score` and `comment_score` (each capped at 650 and doubled).
7. All components are summed to yield `hotness_score`.

## Failures / Exceptions

- If the article id passed to the worker does not match any record, the worker exits silently without error.
- Individual comment scores below -1 are clamped to -1 before summing, preventing a single highly-downvoted comment from collapsing the comment score.
- If `accepted_max` resolves to zero (both article and user `max_score` are 0), no cap is applied and the natural score is used.
