---
id: "01KJ5DQT35P394JJVCSC077ZX5"
name: "reader_views_comment_thread"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/models/comment.rb`
- `app/helpers/comments_helper.rb`
- `app/queries/comments/tree.rb`
- `app/decorators/comment_decorator.rb`
- `app/policies/comment_policy.rb`
- `app/controllers/comments_controller.rb`
- `app/views/comments/index.html.erb` (Template)
- `app/views/comments/_comment.html.erb` (Template)
- `app/views/comments/_comment_proper.html.erb` (Template)
- `app/views/comments/_comment_header.html.erb` (Template)
- `app/views/comments/_comment_footer.html.erb` (Template)
- `app/views/comments/_comment_avatar.html.erb` (Template)
- `app/views/comments/_comment_date.erb` (Template)
- `app/views/comments/_sort_option.html.erb` (Template)
- `app/views/comments/_discussion_lock_reason.html.erb` (Template)
- `app/views/comments/_comment_quality_marker.html.erb` (Template)
- `spec/requests/comments_spec.rb` (Test)
- `spec/models/comment_spec.rb` (Test)
- `spec/helpers/comments_helper_spec.rb` (Test)
- `spec/queries/comments/tree_spec.rb` (Test)
- `spec/decorators/comment_decorator_spec.rb` (Test)
- `spec/policies/comment_policy_spec.rb` (Test)
- `spec/views/comments/_comment.html.erb_spec.rb` (Test)
- `spec/system/comments/user_views_a_comment_spec.rb` (Test)
- `spec/system/comments/user_views_article_comments_spec.rb` (Test)
- `spec/system/comments/like_button_state_after_reply_spec.rb` (Test)
- `spec/requests/comments_with_cache_spec.rb` (Test)
- `app/javascript/packs/commentsDisplay.js`
- `app/javascript/packs/postCommentsPage.js`
- `app/javascript/packs/initializers/initializeCommentDate.js`

## Functional Overview

When a reader navigates to an article's comment section or a comment's permalink, the system builds a nested comment tree using `Comments::Tree`, applies quality-based filtering controlled by `LOW_QUALITY_THRESHOLD` and `HIDE_THRESHOLD`, and renders the thread with author avatars, timestamps, and reaction counts. Signed-out readers see only positive-score comments; signed-in readers see all comments above the hide threshold, with low-quality comments flagged by a visual marker. Admins bypass all quality gates. The thread can be sorted by top score, newest, or oldest. A single comment can serve as the view root by navigating to its permalink, which renders its subtree in isolation. If the article has an active discussion lock, a lock-reason banner is displayed instead of the comment form. If the commentable has been deleted, the thread still renders with a "Comment from a deleted post" notice.

## Design Intent

The three-tier quality system (positive score / above `LOW_QUALITY_THRESHOLD` / above `HIDE_THRESHOLD`) allows the platform to progressively degrade the visibility of low-quality content without immediately erasing it. Signed-out readers receive the cleanest experience, while signed-in users retain access to borderline content with a quality marker. Admins can inspect everything, including content below `HIDE_THRESHOLD`. This prevents bad actors from using low-quality root comments to launder visible child replies, since a childless comment below the hide threshold is a 404 for all non-admin users. The sort system (`top` / `latest` / `oldest`) maps to a simple SQL `ORDER BY` clause built in `Comments::Tree.build_sort_query`, keeping the query layer thin while giving readers meaningful control.

## Key Members

- `LOW_QUALITY_THRESHOLD` — score value of `-75`; comments below this are flagged with a quality marker for signed-in users
- `HIDE_THRESHOLD` — score value of `-400`; childless comments below this are a 404 for non-admins; with children they render as "Comment deleted"
- `VALID_SORT_OPTIONS` — `["top", "latest", "oldest"]`; controls the SQL sort applied by `Comments::Tree`
- `MAX_COMMENTS_TO_RENDER` — `250`; helper threshold above which a high-comment-count notice is shown
- `MIN_COMMENTS_TO_RENDER` — `8`; helper threshold below which the "view all comments" link is hidden

## Scenarios

### Viewing article comments as a signed-out reader

1. Reader navigates to an article's `/comments` path without being signed in.
2. The system builds a comment tree limited to root comments with a non-negative score, excluding all negative-score children.
3. The page renders the nested thread sorted by top score by default, with commenter avatars, publication dates, and reaction counts.
4. The reader sees no quality-marker banners; any comment below zero score is simply absent.

### Viewing article comments as a signed-in reader

1. A signed-in reader visits an article's `/comments` path.
2. The system builds a comment tree that includes negative-score comments (down to `HIDE_THRESHOLD`).
3. Comments with a score below `LOW_QUALITY_THRESHOLD` are rendered with a visible "low quality" quality marker.
4. Comments that fall below `HIDE_THRESHOLD` and have no children are silently omitted; those with children appear as "Comment deleted" with their subtree intact.

### Navigating to a comment's permalink (root view)

1. A reader visits a comment's individual path (e.g., `/:username/comment/:id_code`).
2. The controller identifies the comment as the view root and fetches only its subtree via `Comments::Tree.for_root_comment`.
3. If the comment is below `LOW_QUALITY_THRESHOLD` and has no children, the system raises a 404 for non-admin users.
4. If the comment is hidden by the article author, a banner reads "Comment hidden by post author - thread only visible in this permalink", and the comment body is still shown.
5. The full sub-thread beneath the root comment is rendered, including nested children.

### Sorting the comment thread

1. A reader selects a sort option (top / latest / oldest) from the sort control rendered by `_sort_option.html.erb`.
2. The selected order is passed to `Comments::Tree.for_commentable` as the `order` parameter.
3. `build_sort_query` translates the option into `score DESC`, `created_at DESC`, or `created_at ASC` respectively.
4. The tree is re-rendered with root comments in the chosen order; child comment ordering within a thread is not affected by the sort option.

### Viewing comments when a discussion lock is active

1. A reader navigates to an article that has an active discussion lock.
2. The controller sets `@discussion_lock` from the article's association.
3. The `_discussion_lock_reason.html.erb` partial renders a banner explaining why new comments cannot be submitted.
4. Existing comments remain visible in the thread; only the comment submission form is suppressed.

## Failures / Exceptions

- A comment below `HIDE_THRESHOLD` with no children returns a 404 for all non-admin users, both signed-in and signed-out.
- A comment below `LOW_QUALITY_THRESHOLD` (but above `HIDE_THRESHOLD`) with no children returns a 404 for signed-out users; signed-in users see it with a quality marker.
- Navigating to any comment whose parent article is unpublished or deleted raises a Not Found error for the article path; the direct comment permalink still renders with a "Comment from a deleted post" notice.
- Podcast episode comments use a fixed limit of 12 root comments and do not expose sort options.
- A comment whose score is below zero, or whose commentable's score is below zero, receives a `noindex` meta tag to suppress search-engine indexing of that page.
