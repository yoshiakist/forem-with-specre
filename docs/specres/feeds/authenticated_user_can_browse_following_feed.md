---
id: "01KJV9M1GJDQF9EFPNG89BSKVB"
name: "authenticated_user_can_browse_following_feed"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/stories/feeds_controller.rb`
- `app/views/articles/_feed_nav.html.erb` (Template)
- `spec/requests/stories/feeds_spec.rb` (Test)
- `spec/requests/articles/articles_feed_spec.rb` (Test)

## Functional Overview

When a signed-in user requests `GET /stories/feed` with `type_of=following`, the controller resolves followed user IDs and organization IDs from the user's activity store or cached following lists, then returns articles by those users or organizations with a score above -10. Two sub-variants exist: a "relevant" variant (default) ordered by `hotness_score DESC`, and a "latest" variant (when `timeframe=latest`) ordered by `published_at DESC`. Both are paginated at 25 per page. If the user is not authenticated, the request falls through to the standard signed-out feed.

## Design Intent

The following feed restricts content to authors and organizations the user explicitly follows, providing a focused reading experience. The relevant vs. latest toggle lets users choose between curated ranking and chronological ordering. The logic is inlined in the controller rather than extracted to a service, since it's a straightforward scope composition using followed IDs from the user's activity store.

## Key Members

- `FeedsController#latest_following_feed` — returns followed-author articles ordered by `published_at DESC`.
- `FeedsController#relevant_following_feed` — returns followed-author articles ordered by `hotness_score DESC`.
- `current_user.user_activity` — provides `alltime_users` and `alltime_organizations` lists from the cached activity store.
- `current_user.cached_following_users_ids` / `cached_following_organizations_ids` — fallback when activity store data is unavailable.

## Scenarios

### Authenticated user browses a relevant following feed

1. A signed-in user requests `GET /stories/feed` with `type_of=following` and no `timeframe=latest`.
2. The controller resolves followed user IDs and organization IDs from the user's activity store or cached following lists.
3. Articles by those users or organizations with a score above -10 are returned, ordered by `hotness_score DESC`, paginated 25 per page.

### Authenticated user browses a latest following feed

1. A signed-in user requests `GET /stories/feed` with `type_of=following` and `timeframe=latest`.
2. The controller resolves followed user IDs and organization IDs.
3. Articles are returned ordered by `published_at DESC`, paginated 25 per page.

### Unauthenticated user requests following feed

1. An unauthenticated user requests `GET /stories/feed` with `type_of=following`.
2. The request falls through to the standard signed-out feed (this behavior is not handled here).

## Failures / Exceptions

- If the user has no followed users or organizations, the feed returns an empty result set.
