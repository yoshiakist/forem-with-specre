---
id: "01KJVD2KB5RQGCR6HQH9GGCWBV"
name: "system_detects_reaction_ring_spam"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/spam/reaction_ring_detector.rb`
- `app/workers/spam/reaction_ring_detection_worker.rb`
- `spec/services/spam/reaction_ring_detector_spec.rb` (Test)
- `spec/workers/spam/reaction_ring_detection_worker_spec.rb` (Test)
- `spec/models/reaction_ring_detection_spec.rb` (Test)

## Functional Overview

When a user creates a public article reaction and has accumulated at least 50 such reactions within the past 3 months, the system asynchronously checks whether that user is participating in a coordinated "reaction ring" — a group of users who systematically react to the same authors' articles with suspiciously high concentration and little diversity. The detection service identifies candidate ring members who share at least 2 authors in common with the triggering user, have reaction concentration of 80% or more directed at those shared authors, meet the minimum reaction threshold themselves, and do not exceed 30% self-reactions. If at least 3 such members are found and the group lacks legitimate indicators (follow relationships, shared organization membership, or sufficiently diverse reaction patterns), every member's `reputation_modifier` is halved and an audit `Note` is recorded for each affected user.

## Design Intent

The two-layer gate (worker pre-check then service pre-check) prevents unnecessary database load: the worker guards against calling the detector for ineligible users before instantiating it, and the service re-validates inside `call` to keep the detector self-contained and safe to invoke independently. Legitimate community behavior is explicitly allowed via follow-graph and organization-membership signals, reducing false positives from topic-focused communities. The `until_and_while_executing` Sidekiq lock prevents overlapping jobs for the same user.

## Key Members

- `MIN_REACTIONS_THRESHOLD = 50` — minimum public article reactions in the past 3 months required before any analysis runs
- `MIN_RING_SIZE = 3` — minimum number of co-members required to constitute a ring
- `MIN_AUTHOR_CONCENTRATION = 0.8` — fraction of a candidate member's reactions that must target the shared author set
- `MIN_SHARED_AUTHORS = 2` — minimum number of shared authors between the triggering user and a candidate member
- `MAX_SELF_REACTION_PERCENTAGE = 0.3` — upper bound on self-reactions for a candidate to remain in the ring

## Scenarios

### Ring detection is skipped for ineligible users

1. A user creates a public article reaction.
2. `ReactionRingDetectionWorker` is enqueued via `perform_async` from a model callback only when the user already has 50 or more public article reactions within the past 3 months.
3. Inside the worker, eligibility is re-checked: admins, super moderators, and trusted users are excluded unconditionally.
4. If the user does not pass the threshold check, the worker returns without calling `ReactionRingDetector`.

### No ring found — insufficient shared authors or concentration

1. The worker invokes `Spam::ReactionRingDetector.new(user_id).call`.
2. The detector identifies authors of articles the user has reacted to in the past 3 months, excluding self-reactions.
3. It queries for other users who have reacted to the same authors' articles and shared at least 2 of those authors.
4. For each candidate, it checks that their total recent reactions meet the threshold, that their reaction concentration on the shared author set is at least 80%, and that their self-reaction rate is 30% or below.
5. If no candidates pass all criteria, or fewer than 3 do, `call` returns `false` and no reputation change occurs.

### Coordinated ring confirmed — reputation penalty applied

1. After finding 3 or more qualifying candidate members, the detector calls `is_legitimate_ring?`.
2. It checks whether any member reacts to more than 2 authors outside the shared set (diverse patterns) and, if so, calls `validate_ring_legitimacy`.
3. `validate_ring_legitimacy` counts members who follow the triggering user, are followed by them, or share an organization; if fewer than half of the ring meets those criteria, the ring is confirmed as illegitimate.
4. `adjust_reputation_for_ring` halves the `reputation_modifier` of every ring member and the triggering user, rounding to two decimal places.
5. An audit `Note` with `reason: "reaction_ring_detection"` is persisted for each affected user, and the worker logs the detection and notifies moderators.

### Legitimate community connections prevent penalty

1. Candidate members are found who share the required authors and pass the concentration threshold.
2. However, `validate_ring_legitimacy` finds that 50% or more of those members have a follow relationship with the triggering user or share an organization with them.
3. The ring is classified as a legitimate community; `call` returns `false` and no reputation change occurs.

### Model callback controls when detection is enqueued

1. On creation of a `Reaction` record, an after-create callback fires.
2. The callback checks whether the reaction category is public and whether the reactable is an `Article`; non-article or non-public reactions skip the callback entirely.
3. It also verifies the user meets the 3-month reaction threshold before enqueuing `ReactionRingDetectionWorker.perform_async(user.id)`.

## Failures / Exceptions

- If the `user_id` passed to the worker does not correspond to an existing user, the worker returns immediately without raising.
- If `user_id` is `nil`, the worker returns immediately.
- The Sidekiq job is configured with `retry: 3`, so transient database errors will be retried up to three times before the job is discarded.
