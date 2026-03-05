---
id: "01KJV89SGZ92J93Y580ZM3JQPG"
name: "system_curates_article_quality_via_automated_reactions"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/workers/articles/quality_reaction_worker.rb`
- `spec/workers/articles/quality_reaction_worker_spec.rb` (Test)

## Functional Overview

A Sidekiq background job (`Articles::QualityReactionWorker`) runs periodically to surface high-quality recent content within each discoverable subforem. For every subforem, it collects published full-post articles from the past day that have a non-negative score, have not yet been reacted to by the mascot account, and have not previously been capped via `max_score`. If at least 5 such articles are found, it delegates quality assessment to `Ai::ArticleQualityAssessor`, which returns the best and worst candidates. The system then issues a confirmed `thumbsup` reaction from the mascot to the best article (removing any conflicting `thumbsdown` first). When the eligible pool reaches 12 or more articles, the worst article receives a `max_score` of 15, effectively capping its future algorithmic boost.

## Design Intent

The 5-article minimum ensures the AI assessor has a meaningful comparison set before rendering a judgment. The 12-article threshold for applying `max_score` guards against penalising articles when the comparison pool is too small to reliably identify genuinely low-quality content. Using a dedicated mascot account (rather than an admin user) keeps automated reactions distinguishable from human ones and allows them to be filtered or excluded in other contexts. Excluding articles that already carry a mascot reaction prevents double-processing on repeated job runs without requiring idempotency logic in the AI call.

## Key Members

- `eligible_articles` — published full-post articles from the past day, score >= 0, no prior mascot thumbsup/thumbsdown, `max_score` still 0, ordered by descending score, limit 12
- `assessment[:best]` — article chosen by the AI assessor to receive a `thumbsup`
- `assessment[:worst]` — article chosen by the AI assessor to receive a `max_score` cap (only when pool >= 12)
- `max_score: 15` — the cap value written to the worst article when the 12-article threshold is met

## Scenarios

### No mascot account configured

1. The job runs but `User.mascot_account` returns nil.
2. The worker exits immediately without querying articles or creating any reactions.

### Fewer than 5 eligible articles in a subforem

1. The job fetches published articles from the past day for a subforem, applying score and reaction filters.
2. The count falls below 5.
3. The worker skips AI assessment and produces no reactions for that subforem.

### Between 5 and 11 eligible articles — thumbsup only

1. The worker finds 5–11 eligible articles in a subforem.
2. It calls `Ai::ArticleQualityAssessor` and receives a best and worst candidate.
3. Any existing mascot `thumbsdown` on the best article is removed.
4. A confirmed `thumbsup` reaction is created on the best article by the mascot.
5. No `max_score` is applied because the pool is below the 12-article threshold.
6. The outcome is logged.

### 12 or more eligible articles — thumbsup and max_score cap

1. The worker finds 12 eligible articles (the query limit) in a subforem.
2. It calls `Ai::ArticleQualityAssessor` and receives a best and worst candidate.
3. Any existing mascot `thumbsdown` on the best article is removed.
4. A confirmed `thumbsup` reaction is created on the best article by the mascot.
5. `max_score` is set to 15 on the worst article, capping its algorithmic score ceiling.
6. Both actions are logged together.

### Articles excluded from eligibility

1. Articles older than 1 day, articles with a negative score, articles that are not `full_post` type, and articles that already carry a mascot `thumbsup` or `thumbsdown` are all excluded from the eligible pool before any assessment is performed.
2. If exclusions reduce the pool below 5, the worker takes no action for that subforem.

## Failures / Exceptions

- If `Ai::ArticleQualityAssessor#assess` returns `nil` for `:best`, the worker returns early and issues no reactions.
- The job is configured with `retry: 10` and `lock: :until_and_while_executing`, preventing concurrent runs and allowing automatic retry on transient failures.
