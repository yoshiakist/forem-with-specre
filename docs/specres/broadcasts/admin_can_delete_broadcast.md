---
id: "01KJ6D7VWP7N96ZSZAAXZQ2ZB2"
name: "admin_can_delete_broadcast"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/broadcasts_controller.rb`
- `app/views/admin/broadcasts/show.html.erb`
- `spec/requests/admin/broadcasts_spec.rb` (Test)

## Functional Overview

An authorized admin can permanently delete a broadcast record from the system. The broadcast show page presents a "Destroy" button that triggers a confirmation modal before proceeding. On confirmation, a DELETE request is sent to the broadcasts endpoint; the controller locates the record by ID and destroys it, returning a JSON success message. If destruction fails, a JSON error message is returned instead.

## Scenarios

### Super admin deletes a broadcast

1. A super admin navigates to the broadcast show page.
2. The admin clicks the "Destroy" button, which opens a confirmation modal.
3. The admin confirms the action in the modal.
4. The system sends a DELETE request to `/admin/advanced/broadcasts/:id`.
5. The controller finds the broadcast by ID and destroys it.
6. The system responds with a JSON success message and the broadcast record is removed.

### Single resource admin deletes a broadcast

1. A single resource admin with access to the `Broadcast` resource navigates to the broadcast show page.
2. The admin clicks the "Destroy" button and confirms via the modal.
3. The system sends a DELETE request to `/admin/advanced/broadcasts/:id`.
4. The controller finds the broadcast and destroys it.
5. The system responds with a JSON success message and the broadcast record is removed.

## Failures / Exceptions

- If the broadcast cannot be destroyed (e.g., a model-level validation or callback blocks it), the controller responds with a JSON error message and an HTTP 422 Unprocessable Entity status.
