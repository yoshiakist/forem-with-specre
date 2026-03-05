---
id: "01KJXWBM12SRTZ3BCRGK8G10YT"
name: "user_can_delete_listing"
status: "draft"
---

## Related Files

- `app/models/listing.rb`
- `app/policies/listing_policy.rb`
- `app/controllers/concerns/api/listings_controller.rb`
- `app/controllers/api/v0/listings_controller.rb`
- `app/controllers/api/v1/listings_controller.rb`
- `app/javascript/listings/dashboard/rowElements/actionButtons.jsx`

## Functional Overview

A user may delete a listing they own, or an organization admin may delete a listing belonging to their organization. The listing policy governs authorization by checking whether the requesting user is the listing's author or an organization admin for the listing's organization. Both the V0 and V1 API controllers expose a `destroy` action, and the listings concern defines the shared stub. On the front-end dashboard, each listing row includes a "Delete" button that navigates the user to a delete confirmation URL, providing a confirmation step before the record is permanently removed.

## Design Intent

Authorization for deletion reuses the same `edit?` policy check (aliased as `destroy?` and `delete_confirm?`), ensuring that the permission model for editing and deleting is always in sync. The confirmation URL pattern (`deleteConfirmUrl`) keeps destructive operations behind an explicit user action rather than a single click.

## Scenarios

### Owner deletes their own listing

1. An authenticated user navigates to their listings dashboard.
2. The dashboard renders an action button row for each listing, including a "Delete" link pointing to the delete confirmation URL.
3. The user clicks "Delete" and is taken to the confirmation page.
4. The user confirms, triggering a `DELETE /api/v0/listings/:id` or `DELETE /api/v1/listings/:id` request.
5. The `destroy` action executes and the listing is removed.

### Organization admin deletes a listing belonging to their organization

1. An authenticated user who is an organization admin views the dashboard for a listing owned by their organization.
2. The policy's `destroy?` check passes because the user is an org admin for the listing's organization.
3. The user proceeds through the confirmation flow and the listing is deleted.

### Unauthorized user attempts to delete a listing

1. A user who is neither the listing author nor an organization admin for the listing's organization attempts a delete action.
2. The `ListingPolicy#destroy?` check fails.
3. The request is rejected with an authorization error and the listing is not deleted.

### Draft listing shows "View draft" alongside the delete option

1. A user views the dashboard for a listing marked as a draft (`isDraft: true`).
2. The action buttons component renders both a "View draft" link and a "Delete" link.
3. Deletion proceeds through the same confirmation flow regardless of draft status.

## Failures / Exceptions

- If the current user is not authenticated, the API controllers require authentication before reaching `destroy`, and the request is rejected with an unauthenticated error.
- If the listing does not exist, `Listing.find(params[:id])` raises `ActiveRecord::RecordNotFound`, which is handled by the base API controller with a 404 response.
