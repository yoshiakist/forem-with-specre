---
id: "01KJ9JDSQ6H83982FMRE3T1DQD"
name: "system_computes_user_activity_profile"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/models/user_activity.rb`
- `spec/models/user_activity_spec.rb` (Test)

## Functional Overview

`UserActivity` computes and persists a snapshot of a user's reading and follow behaviour. When `set_activity!` is called, the system fetches the user's 100 most-recent page views, filters them to those where the reader spent more than 29 seconds, and derives a set of recent signals (tags, labels, organizations, subforems, and the raw view list). It also reads the user's all-time follow relationships to populate alltime tags, users, organizations, and subforems. All derived fields are written to the `UserActivity` record in a single `save!` call, and `last_activity_at` is stamped to the current time.

## Key Members

- `recently_viewed_articles` — raw store of up to 100 page-view tuples (article id, created_at, time_tracked_in_seconds), used by recommendation and feed logic.
- `recent_tags` — deduplicated tag names from articles the user actually read (time > 29 s).
- `recent_labels` — up to 5 deduplicated label names from those same articles.
- `recent_organizations` — deduplicated organization ids from recently-read articles.
- `recent_users` — deduplicated author ids from recently-read articles.
- `recent_subforems` — subforem ids from recently-read articles, **not** deduplicated so that volume per subforem can be tabulated downstream.
- `alltime_tags` — tag names from the user's followed tags (`cached_followed_tag_names`).
- `alltime_users` — ids of users the current user follows.
- `alltime_organizations` — ids of organizations the current user follows.
- `alltime_subforems` — ids of subforems the current user follows.
- `last_activity_at` — timestamp of the last profile recomputation.

## Scenarios

### Computing a fresh activity snapshot

1. The caller invokes `set_activity!` on an existing `UserActivity` record.
2. The system queries the user's page views, ordered most-recent first, limited to 100 rows.
3. From those rows, the system selects only the articles where `time_tracked_in_seconds` exceeds 29 seconds.
4. For the filtered articles the system computes: deduplicated tag names, up to 5 deduplicated label names, deduplicated organization ids, deduplicated author ids, and subforem ids (with duplicates kept to preserve volume).
5. The system writes the full raw view list into `recently_viewed_articles`, stamps `last_activity_at` to the current time, and persists all fields in one save.

### Populating all-time follow signals

1. During the same `set_activity` call, the system reads the user's followed tag names via `cached_followed_tag_names`.
2. The system queries the `follows` table for all users, organizations, and subforems the current user follows and collects their ids.
3. These are stored in `alltime_tags`, `alltime_users`, `alltime_organizations`, and `alltime_subforems` on the record.

### Retrieving a blended tag list

1. A caller invokes `relevant_tags` with optional `recent_tag_count` (default 5) and `all_time_tag_count` (default 5).
2. The system takes the first `recent_tag_count` entries from `recent_tags` and the first `all_time_tag_count` entries from `alltime_tags`.
3. It returns these two slices concatenated as a single array (no additional deduplication at this layer).

### Updating an existing record

1. When `set_activity!` is called on an already-persisted `UserActivity`, the system overwrites all activity fields in place.
2. No new record is created; the existing row is updated.
