---
id: "01KJ5DK8KFA45BXJWFAD1VNYMS"
name: "user_can_retrieve_comments_via_api"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/api/v0/comments_controller.rb`
- `app/controllers/api/v1/comments_controller.rb`
- `app/controllers/concerns/api/comments_controller.rb`
- `app/models/comment.rb`
- `spec/requests/api/v0/comments_spec.rb` (Test)
- `spec/requests/api/v1/comments_spec.rb` (Test)
- `spec/requests/api/v1/docs/comments_spec.rb` (Test)

## Functional Overview

The API exposes two read-only endpoints — `GET /api/comments` and `GET /api/comments/:id` — that allow clients to retrieve comments as nested, threaded conversations. The index action accepts either an article identifier (`a_id`) or a podcast episode identifier (`p_id`) and returns all root-level comments with their full descendant trees arranged by id. The show action accepts a single base-26-encoded comment id and returns that comment together with all its descendants as a subtree. Both actions set HTTP cache-control headers and Surrogate-Key response headers that enumerate every comment's cache key, enabling precise CDN invalidation. Pagination on the index action is opt-in: it is applied only when the `page` parameter is present and positive, defaulting to 50 comments per page.

## Design Intent

Deleted and hidden comments are intentionally kept in the thread so that descendant comments remain reachable and the conversation thread is not silently broken. Their body is replaced with a placeholder string and their user information is cleared, preserving structural integrity without exposing removed content.

The surrogate-key headers are built by recursively traversing the already-in-memory comment tree rather than issuing additional SQL queries, avoiding N+1 problems at the CDN cache-invalidation layer.

## Key Members

- `DEFAULT_PER_PAGE` — default page size of 50, used only when pagination is active.
- `ATTRIBUTES_FOR_SERIALIZATION` — the fixed set of model attributes selected from the database: `id`, `processed_html`, `user_id`, `ancestry`, `deleted`, `hidden_by_commentable_user`, `created_at`.

## Scenarios

### Client retrieves all comments for an article

1. Client sends `GET /api/comments?a_id=<article_id>`.
2. The system locates the article and loads its full comment tree, ordered by id, including user profile associations.
3. The response body is a flat array of root-level comment objects; each root comment carries its descendants nested under a `children` key, recursively.
4. The response includes a `Surrogate-Key` header listing the article's cache key, the `comments` table key, and every individual comment's cache key.

### Client retrieves all comments for a podcast episode

1. Client sends `GET /api/comments?p_id=<episode_id>`.
2. The system locates the podcast episode and returns its comment tree in the same threaded format as for articles.

### Client paginates the comment list

1. Client sends `GET /api/comments?a_id=<article_id>&page=2&per_page=10`.
2. Because the `page` parameter is a positive integer, the system applies Kaminari pagination to the flat list of root-level comments.
3. The response contains the slice of root-level comments for the requested page, each still carrying its full child tree.
4. Without a `page` parameter, all comments are returned regardless of `per_page`.

### Client retrieves a single comment and its descendants

1. Client sends `GET /api/comments/:id` where `:id` is the base-26-encoded comment identifier.
2. The system builds the subtree rooted at that comment, loading all descendants and their user profiles.
3. The response body is a single comment object with descendants nested under `children`.
4. The `Surrogate-Key` header lists the `comments` table key and every comment in the subtree.

### Deleted or hidden comment appears with redacted content

1. A comment in the thread has been marked as deleted or hidden by the content author.
2. The comment still appears at its position in the thread so descendants remain accessible.
3. Its `body_html` field is replaced with a fixed placeholder string; its `user` field is returned empty.
4. Child comments beneath the redacted comment are still present and fully rendered.

## Failures / Exceptions

- If the supplied `a_id` does not match any article, or `p_id` does not match any podcast episode, the response is `404 Not Found`.
- If the supplied comment `:id` for the show action does not resolve to an existing comment, the response is `404 Not Found`.
