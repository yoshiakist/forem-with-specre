---
id: "01KJ9KAVAKYF7567P2ES4HD61W"
name: "moderator_can_delete_user"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `app/services/moderator/delete_user.rb`
- `spec/services/moderator/delete_user_spec.rb` (Test)
- `spec/system/admin/admin_deletes_user_spec.rb` (Test)

## Functional Overview

When a moderator triggers user deletion, the system enqueues an asynchronous background job via `Users::DeleteWorker` to fully remove the user and all associated data. The `Moderator::DeleteUser` service provides a `.call` class method that accepts a user object and schedules the deletion asynchronously. It also exposes a private synchronous path used internally, which performs the deletion immediately in the same process. The behavior cascades through the user's data, removing records such as follows and articles as part of the deletion process.

## Design Intent

The deletion is handled asynchronously via a background worker to avoid blocking the moderator's request during potentially expensive cascading deletes. The `true` flag passed to `Users::DeleteWorker` signals that this is a moderator-initiated hard deletion (as opposed to a soft delete or self-initiated account removal).

## Scenarios

### Moderator deletes a user

1. A moderator initiates deletion of a target user account.
2. The system enqueues a background worker job to perform the full deletion of that user.
3. The worker executes and permanently removes the user record from the database.

### User's associated follows are removed

1. A moderator deletes a user who has follow relationships (as follower and as followable).
2. The background worker runs and removes all follow records linked to the deleted user.
3. No orphaned follow records remain after deletion.

### User's articles are removed

1. A moderator deletes a user who has authored articles.
2. The background worker runs and removes all articles belonging to the deleted user.
3. No articles authored by the deleted user remain in the system.
