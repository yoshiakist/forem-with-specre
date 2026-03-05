---
id: "01KJY12PD73C5DE32KJHRMCBKP"
name: "user_archives_reading_list_item"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/controllers/reading_list_items_controller.rb`
- `app/javascript/readingList/readingList.jsx`
- `app/javascript/readingList/components/ItemListItemArchiveButton.jsx`
- `spec/requests/reading_list_items_spec.rb` (Test)
- `app/javascript/readingList/components/__tests__/ItemListItemArchiveButton.test.jsx` (Test)

## Functional Overview

When a signed-in user clicks the archive button on a reading list item, the client sends a PUT request to `/reading_list_items/:id` with the current view status. The server toggles the reaction's status between `archived` and `valid`: if the item is currently archived, it becomes valid again; otherwise it is archived. After saving, the user's `last_reacted_at` timestamp is updated. On the client side, the item is immediately removed from the current list view and a snackbar notification informs the user whether the item is being archived or unarchived. The archive button component is a simple presentational element that delegates its click behavior to the parent reading list component.

## Design Intent

The toggle logic is driven by the `current_status` parameter sent by the client, which reflects the view the user is currently on (`valid,confirmed` or `archived`). This avoids the need for the server to re-fetch the item's current state, and keeps the status transition logic straightforward: if the caller says the current status is `archived`, the server sets it to `valid`; otherwise it sets it to `archived`. The client performs an optimistic update by removing the item from the displayed list immediately, before the server responds, to give instant feedback.

## Scenarios

### User archives an item from the valid reading list

1. The user is on the main reading list view (showing valid and confirmed items).
2. The user clicks the archive button on an item.
3. The client sends a PUT request to `/reading_list_items/:id` with no `current_status` parameter (or with status reflecting the valid view).
4. The server sets the reaction status to `archived` and updates the user's `last_reacted_at` timestamp.
5. The item is immediately removed from the displayed list and a snackbar shows "Archiving...".

### User unarchives an item from the archive view

1. The user is on the archive view (showing archived items).
2. The user clicks the unarchive button on an item.
3. The client sends a PUT request to `/reading_list_items/:id` with `current_status` set to `archived`.
4. The server sets the reaction status to `valid` and updates the user's `last_reacted_at` timestamp.
5. The item is immediately removed from the archive view and a snackbar shows "Unarchiving...".

### Unauthorized user attempts to archive another user's item

1. A signed-in user sends a PUT request to `/reading_list_items/:id` for a reaction that belongs to a different user.
2. The server raises a `Pundit::NotAuthorizedError` and denies the action.

## Failures / Exceptions

- If the reaction does not belong to the currently signed-in user, the request is rejected with a `Pundit::NotAuthorizedError`.
