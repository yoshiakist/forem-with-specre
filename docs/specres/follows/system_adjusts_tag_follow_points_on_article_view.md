---
id: "01KJ1XE6K4BWFZTPRP6E0M6244"
name: "system_adjusts_tag_follow_points_on_article_view"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/workers/follows/update_points_worker.rb`
- `spec/workers/follows/update_points_worker_spec.rb` (Test)
- `spec/lib/data_update_scripts/populate_explicit_follow_points_spec.rb` (Test)

## Functional Overview

When a user views or reacts to an article, the system asynchronously recalculates the implicit follow points for each tag on that article that the user already follows. The worker (`Follows::UpdatePointsWorker`) looks at the user's recent engagement history — specifically the last 100 positively-reacted articles and the last 100 articles read for 45 or more seconds — to count how many of those articles share the tag. It converts that count into a logarithmic score, boosted by an inverse-popularity factor that rewards niche tags over widely-used ones. Simultaneously, to prevent any single interest spike from dominating a user's feed permanently, the worker applies a small decay (0.98×) to a random sample of five of the user's other tag follows, allowing stale interests to fade over time.

## Design Intent

The split between `implicit_points` and `explicit_points` allows the system to separate organic engagement signals (implicit) from deliberate user choices (explicit follow strength). Using a logarithmic scale for implicit points prevents a single burst of activity from creating an outsized and persistent weight. The random 0.98× decay on unrelated follows acts as a soft re-balancing mechanism, avoiding a bias where early or high-volume tags dominate forever without requiring a full recomputation of all follows on every job run.

## Key Members

- `implicit_points` on `Follow` — the dynamically computed engagement score updated by this worker on each run; combined with `explicit_points` to produce `points`
- `explicit_points` on `Follow` — the user-intent score (set separately); not modified by this worker
- `points` on `Follow` — the combined score (`implicit_points + explicit_points`) used for feed ranking

## Scenarios

### Recalculating implicit points for followed tags on an article

1. The worker receives an article ID and a user ID; if either record is missing, it exits immediately.
2. It applies a small decay to five randomly chosen tag follows of the user (multiplying their `points` by 0.98) to allow stale interests to diminish.
3. For each tag on the article that the user already follows or anti-follows, it recomputes implicit points.
4. The implicit point calculation inspects the user's last 100 positively-reacted articles and last 100 long-read articles (45+ seconds), counts how many contain the tag, then computes a logarithmic score incorporating an inverse-popularity bonus.
5. The resulting `implicit_points` is saved on the `Follow` record; the model combines it with `explicit_points` to update `points`.

### Awarding bonus weight to niche tags

1. When computing the inverse-popularity bonus, the worker fetches the platform-wide top 100 tags by hotness score (cached).
2. If the tag appears in that list, its index position (lower = more popular) becomes the bonus value; a tag ranked first receives a bonus of 0, and lower-ranked tags receive progressively larger bonuses.
3. If the tag is not in the top 100 at all, it receives a bonus equal to 150% of the list size, giving niche tags the largest boost.
4. This bonus is added to the occurrence count before the logarithm is applied, so it blunts but does not eliminate the effect of raw engagement volume.

### Decaying non-involved tag follows

1. Before recalculating any tag's points, the worker selects five tag follows of the user at random (using a random database order).
2. Each selected follow's `points` column is updated directly to 98% of its current value.
3. This decay runs regardless of which tags appeared on the article, ensuring long-neglected interests slowly lose weight across repeated job invocations.

## Failures / Exceptions

- If the article or user record cannot be found by ID, `perform` returns early without performing any updates.
- The `+ 1` inside `finalized_points` ensures the argument to `Math.log` is always at least 1, preventing a result of negative infinity when occurrence count and bonus are both zero.
