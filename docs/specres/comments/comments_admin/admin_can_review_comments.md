---
id: "01KJ43VPQ39TQMBTTNBVQRBZQW"
name: "admin_can_review_comments"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/admin/comments_controller.rb`
- `app/views/admin/comments/index.html.erb` (Template)
- `app/views/admin/comments/show.html.erb` (Template)
- `app/views/admin/comments/_comment.html.erb` (Template)
- `spec/requests/admin/comments_spec.rb` (Test)

## Functional Overview

Admin users can review comments through a paginated list view and a detail view. The index action loads comments with their associated user, commentable resource, and reactions, and optionally sorts them by top public reaction count within a rolling time window when a `toplast-` prefixed state parameter is provided; otherwise comments are ordered by creation date descending. The show action loads a single comment and its associations. For every comment rendered, the controller calculates a flag count representing the number of non-invalidated "vomit" privileged reactions attached to that comment. Access to both actions is restricted to users authorized through `InternalPolicy`.

## Design Intent

The flag count (named `countable_vomits`) is computed in the controller rather than in a database query so that the already-eager-loaded reactions association can be reused, avoiding additional queries per comment. N+1 queries from eager-loading are further suppressed by temporarily disabling the Bullet gem via an `around_action` callback.

## Key Members

- `@comments` — paginated collection of `Comment` records, 50 per page, eager-loaded with user, commentable, and reactions
- `@comment` — single `Comment` record for the show view, eager-loaded with user, commentable, and reactions
- `@countable_vomits` — hash mapping comment ID to its count of valid "vomit" privileged reactions

## Scenarios

### Viewing the paginated comment list (default order)

1. An authenticated admin navigates to the admin comments index without a `state` parameter.
2. The controller loads the 50 most recently created comments, eager-loading their user, commentable, and reactions.
3. For each comment, it counts reactions in the privileged category whose `category` is `"vomit"` and whose `status` is not `"invalid"`, storing the count by comment ID.
4. The index template renders a paginated list; each comment card shows the author, the parent article, privileged reaction counts (thumbsup, thumbsdown, vomit flags), public like count, comment body, and a link to the detail view.

### Viewing the comment list sorted by top reactions within a time window

1. An authenticated admin navigates to the index with a `state` parameter prefixed with `"toplast-"` followed by a number of days (e.g., `toplast-7`).
2. The controller interprets the suffix as a day count and loads comments created within that window, ordered by `public_reactions_count` descending, paginated 50 per page.
3. Flag counts are calculated and the same index template is rendered.

### Viewing a single comment in detail

1. An authenticated admin follows the "View details" link for a specific comment.
2. The controller loads that comment with its user, commentable, and reactions associations, and computes its flag count.
3. The show template renders the comment card. Below it, a tabbed panel lists privileged reactions: the "Flags" tab shows non-invalidated vomit reactions in reverse chronological order; the "Quality reactions" tab shows the remaining privileged reactions.

### Access control enforcement

1. Any request to the comments index or show action triggers `authorize_admin`, which calls `InternalPolicy` to check the `access?` permission on `Comment`.
2. Users who do not pass the policy check are denied access before any comment data is loaded.

## Failures / Exceptions

- If a comment's `commentable` association is nil (e.g., the parent article was deleted), the comment card header is suppressed and only the comment body and footer are rendered.
