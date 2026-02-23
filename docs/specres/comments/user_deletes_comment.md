---
id: "01KJ5DZ0J6MPMBE92886V9ZXXZ"
name: "user_deletes_comment"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/comments_controller.rb`
- `app/models/comment.rb`
- `app/policies/comment_policy.rb`
- `spec/requests/comments_destroy_spec.rb` (Test)
- `spec/system/comments/user_delete_a_comment_spec.rb` (Test)
- `app/views/comments/delete_confirm.html.erb` (Template)

## Functional Overview

When the comment's author chooses to delete their comment, the system first shows a confirmation page. On confirmation, if the comment has no replies, it is permanently removed from the database; if replies exist, it is soft-deleted by setting a `deleted` flag so the thread structure is preserved and descendant notifications are updated. Either path removes any notifications associated with the deleted comment, busts relevant caches, and redirects the author back to the commentable resource (or their profile if none exists).

## Design Intent

The hard-delete vs. soft-delete strategy is based on whether the comment has children. Permanently destroying a childless comment keeps the database clean. Soft-deleting a parent that has replies preserves thread integrity — child comments remain readable and can still display their context — while the deleted comment is shown as `[deleted]` to readers.

## Key Members

- `Comment#is_childless?` — determines which deletion path is taken
- `Comment#deleted` — boolean flag set to `true` on soft-delete; triggers descendant notification updates and notification removal
- `Comment#before_destroy_actions` — touches `last_comment_at` on the commentable, updates ancestor timestamps, and busts comment cache before hard-delete
- `Comment#after_destroy_actions` — busts the user cache and touches the user's `last_comment_at` after hard-delete

## Scenarios

### Author navigates to the delete confirmation page

1. The signed-in user visits the delete confirmation URL for their own comment (`/:username/comment/:id_code/delete_confirm`).
2. The system authorizes the request, confirming the current user is the comment's author.
3. The confirmation page is rendered, asking the user to confirm the deletion.

### Author deletes a childless comment (hard delete)

1. The author confirms deletion on the confirmation page.
2. The system authorizes the action and determines the comment has no replies.
3. The comment is permanently destroyed; cache is busted and the user's activity timestamp is updated.
4. The author is redirected to the commentable resource's path (or their profile) with a success notice.

### Author deletes a comment that has replies (soft delete)

1. The author confirms deletion on the confirmation page.
2. The system authorizes the action and determines the comment has one or more child replies.
3. The comment's `deleted` flag is set to `true` and saved; the record is not removed from the database.
4. Notifications for the comment are removed, and notifications for all descendant comments are updated to reflect the change.
5. The comment now appears as `[deleted]` to readers; the reply thread remains intact.
6. The author is redirected to the commentable resource's path with a success notice.

### System redirects to article after deletion via UI

1. After the author clicks "Delete" on the confirmation page, the comment is destroyed.
2. The browser is redirected to the article page that contained the comment.

## Failures / Exceptions

- A user who is not the comment's author receives an authorization denial (Pundit policy `destroy?` requires `user_author?`). The request is rejected and access to both the delete confirmation page and the destroy action is blocked.
