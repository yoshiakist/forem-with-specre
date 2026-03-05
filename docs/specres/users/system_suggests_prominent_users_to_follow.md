---
id: "01KJBGNEV9X0CNE7X8M862SC2Z"
name: "system_suggests_prominent_users_to_follow"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/queries/users/suggest_prominent.rb`
- `spec/queries/users/suggest_prominent_spec.rb` (Test)

## Functional Overview

When the system needs to suggest users to follow, it selects up to 20 prominent users by identifying authors of high-scoring, recently published articles from the current subforem. If the requesting user follows any tags, the search is scoped to articles matching those tags; otherwise, featured articles are used as the pool. Authors are ranked by article score, the requesting user is excluded, and the result is returned as a randomized sample. If the candidate pool is too small (fewer than 4 users), the system falls back to the highest-scored users site-wide.

## Design Intent

Tag-based filtering personalizes suggestions for established users with known interests, while the featured-articles fallback serves new users and forems without sufficient tag-based signal. The fallback to top-scored users site-wide guards against brand-new forem instances where recent articles are scarce.

## Key Members

- `RETURNING` — maximum number of users returned (20); also controls intermediate pool sizes
- `attributes_to_select` — optional list of columns to include in the returned User records, allowing callers to avoid loading full objects

## Scenarios

### Suggesting users when the requesting user follows tags

1. The caller provides a user who follows one or more tags.
2. The system looks up recently published, high-scoring articles in the current subforem that carry any of those tags, using the configured feed lookback window.
3. The authors of those articles (excluding the requesting user) are collected, ranked by score, and a random sample of up to 20 is selected.
4. The system returns those users joined with their profile, limited to the requested attributes.

### Suggesting users when the requesting user follows no tags

1. The caller provides a user who follows no tags.
2. The system selects recently published, high-scoring featured articles from the current subforem within the configured lookback window.
3. The authors of those articles (excluding the requesting user) are sampled and returned as above.

### Falling back when the candidate pool is too small

1. After filtering articles, fewer than 4 unique non-self authors are found.
2. The system falls back to the top-scored users across the entire platform, limited to 40 candidates.
3. The requesting user is excluded from this fallback list, and up to 20 users are returned.

### Returning only selected attributes

1. The caller passes a list of attribute names (e.g., `id`, `username`) via `attributes_to_select`.
2. The returned User records contain only those columns.
