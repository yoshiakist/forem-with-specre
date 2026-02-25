---
id: "01KJBGS95JE0MXBB7NXGXDKTE4"
name: "system_suggests_users_for_sidebar"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/users/suggest_for_sidebar.rb`
- `spec/services/users/suggest_for_sidebar_spec.rb` (Test)
- `spec/requests/user/user_suggestions_spec.rb` (Test)

## Functional Overview

When a signed-in user views a page with a given tag context, the system suggests up to 40 other users for display in the sidebar. Suggestions are drawn from authors of recently published, tag-matching articles that have met a minimum public reaction threshold. The result blends a reputation-ranked list and a randomly ordered list to balance quality and variety. Results are cached per user and tag for five days to avoid repeated database queries.

## Design Intent

The minimum reaction count threshold (25 in production, 0 in development) is a legacy tuning parameter carried over from DEV.to. It may not suit smaller communities and is marked as a known trade-off in the source.

## Key Members

- `user` — The signed-in user requesting suggestions; suggestions exclude users already followed by this user.
- `given_tag` — The tag used to scope candidate articles and shape the cache key.
- `minimum_reaction_count` — Reaction floor for candidate articles; 25 in production, 0 in development.

## Scenarios

### Returns suggestions for a signed-in user with matching tagged articles

1. A signed-in user requests suggestions with a given tag.
2. The system looks up recently published articles tagged with that tag that have enough public reactions and whose authors the user does not yet follow.
3. The system builds a combined list of up to 20 reputation-ranked authors and up to 20 randomly ordered authors, deduplicating the result.
4. The combined list is stored in the cache keyed by tag and user identity, then used to fetch the corresponding user records.
5. The system returns those user records, each carrying only id, name, username, and profile image.

### Returns an empty result when no signed-in user is present

1. The caller invokes the service without a user (nil).
2. The system skips all database queries and immediately returns an empty relation.

### Returns an empty result when no candidate articles match

1. A signed-in user requests suggestions with a given tag.
2. No published articles exist for that tag that satisfy the reaction threshold and recency window, or all matching authors are already followed.
3. The candidate pool is empty, so the combined list is empty.
4. The system returns an empty relation.

### Serves cached suggestions on subsequent calls

1. A signed-in user requests suggestions with a given tag a second time within 120 hours.
2. The system finds a cached result keyed by tag and user, skipping the database queries for candidate articles.
3. The cached user IDs are used to return the same set of user records.

## Failures / Exceptions

- If the user has never followed anyone, `last_followed_at` is nil; the cache key still incorporates this nil value, so the key remains unique per user.
