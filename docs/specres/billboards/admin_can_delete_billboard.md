---
id: "01KJ6EE55AAZWW43YVSXTJ4K72"
name: "admin_can_delete_billboard"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/billboards_controller.rb`
- `app/models/billboard.rb`
- `spec/requests/admin/billboards_spec.rb` (Test)

## Functional Overview

When an admin sends a DELETE request for a specific billboard, the controller finds the record by its ID and attempts to destroy it. On success, it returns a JSON response with a localized success message and HTTP status 200. If destruction fails (e.g., due to a callback or validation preventing deletion), it returns a JSON response with a localized error message and HTTP status 422. Deleting a billboard also cascades to destroy all associated `billboard_events` records, as defined by the `dependent: :destroy` association on the `Billboard` model.

## Design Intent

The action responds with JSON rather than a redirect or HTML page, which is consistent with a frontend that handles deletion via an asynchronous request and updates the UI without a full page reload. Returning 422 on failure preserves the ability for the client to detect and surface deletion errors gracefully.

## Scenarios

### Successful deletion by a super admin

1. A super admin sends a DELETE request to `/admin/customization/billboards/:id` for an existing billboard.
2. The controller finds the billboard by the given ID.
3. The billboard is destroyed; all associated `billboard_events` are also destroyed via cascade.
4. The controller responds with HTTP 200 and a JSON body containing a localized success message.

### Successful deletion by a single resource admin

1. A user with the single resource admin role for `Billboard` sends a DELETE request to `/admin/customization/billboards/:id`.
2. The controller finds the billboard by the given ID.
3. The billboard and its associated `billboard_events` are destroyed.
4. The controller responds with HTTP 200 and a JSON body containing a localized success message.

### Failed deletion

1. An admin sends a DELETE request for an existing billboard.
2. The controller finds the billboard and attempts to destroy it.
3. Destruction fails (e.g., a callback prevents it).
4. The controller responds with HTTP 422 and a JSON body containing a localized error message.

## Failures / Exceptions

- If the billboard cannot be destroyed, the action renders `{ error: <localized message> }` with status `422 Unprocessable Entity` rather than raising an exception.
