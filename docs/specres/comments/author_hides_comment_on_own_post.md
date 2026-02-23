---
id: "01KJ5DR9SK7NZF4GCYBZD5RM92"
name: "author_hides_comment_on_own_post"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/comments_controller.rb`
- `app/models/comment.rb`
- `app/policies/comment_policy.rb`
- `app/views/comments/_hide_comments_modal.html.erb` (Template)
- `spec/requests/shared_examples/comment_hide_or_unhide_request.rb` (Test)

## Functional Overview

The author of a post (the commentable owner) can hide or unhide any comment left on their own post, unless that comment was written by the staff account. When a comment is hidden, the `hidden_by_commentable_user` flag is set on the comment and all of its notifications are removed. The post's `any_comments_hidden` flag is updated to reflect whether at least one hidden comment still exists. Optionally, hiding a comment can cascade to all of its descendants in a single request. Unhiding a comment clears the flag and recalculates `any_comments_hidden` based on the remaining hidden state of sibling comments.

## Design Intent

- **Staff account protection:** Comments written by the staff account cannot be hidden by the post author, preserving the platform's ability to communicate with users through official moderation comments without risk of suppression.
- **`any_comments_hidden` tracking:** The post-level flag lets the UI quickly indicate that some comments have been moderated without querying every comment. On unhide, the flag is recomputed from the actual state of all comments rather than blindly toggled, so it remains accurate even when only a subset of hidden comments is restored.
- **Notification removal on hide:** Removing notifications when a comment is hidden prevents readers from being alerted to content the post author has chosen to suppress.

## Key Members

- `hidden_by_commentable_user: Boolean` — per-comment flag indicating the post author has hidden this comment
- `any_comments_hidden: Boolean` — post-level flag indicating at least one comment on the post is currently hidden

## Scenarios

### Hide a single comment

1. The post author sends a hide request for a specific comment on their post.
2. The system authorizes the request, confirming the requester owns the post and the comment was not written by the staff account.
3. The comment's hidden flag is set to true.
4. The post's `any_comments_hidden` flag is set to true.
5. All notifications for that comment are removed.
6. The system responds with a JSON payload confirming the comment is hidden.

### Hide a comment and all its descendants

1. The post author sends a hide request for a comment, including a `hide_children` parameter set to `"1"`.
2. The system hides the target comment as described in the single-comment scenario.
3. The system iterates over every descendant of the target comment and sets each one's hidden flag to true.
4. Descendant notifications are removed as part of their individual updates.

### Unhide a comment

1. The post author sends an unhide request for a previously hidden comment.
2. The system authorizes the request using the same rules as hide.
3. The comment's hidden flag is cleared.
4. The system recalculates `any_comments_hidden` for the post by checking whether any other comment on the post is still hidden; the flag is set accordingly.
5. The system responds with a JSON payload confirming the comment is no longer hidden.

### Non-author or unauthenticated user attempts to hide

1. A request to hide or unhide a comment arrives from a user who is not the post author, or from an unauthenticated session.
2. The authorization check fails: unauthenticated requests receive a 401 response; authenticated non-authors receive a Pundit authorization error.
3. No changes are made to any comment or post flags.

## Failures / Exceptions

- **Staff account comment:** If the target comment was written by the staff account, the policy denies the hide action regardless of who the post author is. The request is treated as unauthorized.
- **Unauthorized requester:** Any user who is not the owner of the post that contains the comment is denied both hide and unhide actions by the Pundit policy.
- **Validation failure on save:** If saving the comment fails (e.g., a model validation error), the system returns a 422 response with a sentence-form error message derived from the comment's validation errors.
