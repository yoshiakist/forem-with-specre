---
id: "01KJ5E2R9YYMDP0Q8147BK9704"
name: "admin_soft_deletes_comment"
status: "draft"
---

## Related Files

- `app/controllers/comments_controller.rb`
- `app/models/comment.rb`
- `app/policies/comment_policy.rb`

## Functional Overview

When an admin invokes the delete action on a comment, the system marks the comment as deleted by setting its `deleted` flag to `true` and saving the record — it does not destroy the database row. After a successful save, the user is redirected to the commentable resource's path (e.g., the article page) with a success notice. If the commentable resource has no resolvable path, the admin is redirected to the comment's own moderation path with an error flash. Every invocation of this action is recorded in the moderation audit log regardless of outcome. Downstream effects triggered by the model include removal of all associated notifications and updates to any descendant notification records.

## Design Intent

Soft deletion preserves thread integrity: the comment row and its replies remain in the database, allowing the display layer to render a placeholder and keeping reply chains coherent. This approach avoids orphaning child comments that would otherwise lose their parent reference. The audit log entry written after every admin delete call provides an accountability trail, enabling retrospective review of moderation decisions without relying solely on application logs.

## Key Members

- `Comment#deleted` — boolean flag; setting it to `true` marks the comment as soft-deleted without removing the row
- `Comment#remove_notifications` — removes all associated `Notification` records when the comment is deleted or hidden
- `Comment#update_descendant_notifications` — updates notifications on descendant comments after the parent is marked deleted
- `CommentPolicy#admin_delete?` — gate that restricts this action to any-admin users only
- `Audit::Logger.log(:moderator, ...)` — records the acting admin and request params for the moderation audit trail

## Scenarios

### Successful soft delete with redirect to commentable

1. An admin navigates to a comment's moderation page and triggers the delete action.
2. The system authorizes the request via the policy, confirming the current user holds any admin role.
3. The comment's deleted flag is set to true and the record is saved.
4. The model callbacks fire: descendant notifications are updated and all notifications for the comment are removed without delay.
5. The system resolves the commentable resource's path and redirects the admin there, showing a success flash message.
6. The audit logger records the moderation event with the acting user and request parameters.

### Soft delete when commentable has no resolvable path

1. An admin triggers the delete action on a comment whose parent resource has been removed or has no path.
2. Authorization succeeds and the comment is saved with the deleted flag set to true.
3. The system attempts to resolve the commentable path but finds none.
4. The admin is redirected to the comment's own moderation path (`<comment_path>/mod`) with an error flash message.
5. The audit logger still records the moderation event.

### Audit logging on every admin delete

1. An admin calls the delete action on any comment.
2. Regardless of whether the save succeeds or the redirect target is found, the `after_action` callback fires after the response is prepared.
3. The system writes a `:moderator` audit entry that includes the current user identity and a copy of the request parameters.

## Failures / Exceptions

- **Non-admin attempt:** Any user who does not hold an admin role will be rejected at the policy layer (`CommentPolicy#admin_delete?` returns false), raising an authorization error before any state is modified.
- **Save failure:** If saving the comment with the deleted flag fails (e.g., due to a validation error), the system redirects the admin to the comment's moderation path with an error flash; no audit entry is written because the `after_action` callback only runs on a completed response cycle, but the comment state is not changed.
- **Missing commentable fallback:** When the commentable resource exists but provides no path, the system falls back to the moderation path redirect rather than raising an error, ensuring the admin always receives a navigable response.
