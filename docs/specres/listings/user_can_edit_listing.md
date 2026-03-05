---
id: "01KJXWGTKXY2KHWQQ23XG2PNZF"
name: "user_can_edit_listing"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/models/listing.rb`
- `app/policies/listing_policy.rb`
- `app/controllers/concerns/api/listings_controller.rb`
- `app/controllers/api/v0/listings_controller.rb`
- `app/controllers/api/v1/listings_controller.rb`
- `app/javascript/listings/listingForm.jsx`
- `app/javascript/listings/components/Title.jsx`
- `app/javascript/listings/components/BodyMarkdown.jsx`
- `app/javascript/listings/components/ListingTagsField.jsx`
- `app/javascript/packs/listingForm.jsx`
- `app/javascript/listings/__tests__/BodyMarkdown.test.jsx` (Test)
- `app/javascript/listings/__tests__/ListingTagsField.test.jsx` (Test)

## Functional Overview

A logged-in user can edit an existing classified listing they own, or that belongs to an organization they administer. The `ListingForm` Preact component detects whether a listing `id` is present; when it is, the form renders in edit mode showing the current title, body markdown, and tags pre-populated from the listing data. Authorization is enforced by `ListingPolicy`, which grants edit access only to the original author or an organization admin. Both the v0 and v1 API controllers authenticate the user before handling an update request, load the target listing via `set_and_authorize_listing`, and delegate the update action through the shared `Api::ListingsController` concern.

## Design Intent

The `ListingForm` component reuses the same field components (`Title`, `BodyMarkdown`, `ListingTagsField`) for both create and edit flows, branching on whether `id` is `null`. This avoids duplicating UI logic while keeping the edit path lightweight — notably omitting category selection and expiry date fields, which are commented as work-in-progress for the edit view. Policy authorization is extracted into `ListingPolicy` using Pundit so that controller and API layers share a single source of truth for permission checks.

## Key Members

- `id` (state, `ListingForm`) — `null` indicates create mode; a non-null value triggers edit mode rendering
- `title`, `bodyMarkdown`, `tagList` (state, `ListingForm`) — fields pre-populated from the existing listing and bound to their respective field components
- `edit?` / `update?` (`ListingPolicy`) — grants access when the current user is the listing author or an organization admin for the listing's organization
- `set_and_authorize_listing` (controllers) — loads the `Listing` record by `params[:id]` before the update action

## Scenarios

### Authorized user opens the edit form

1. A user navigates to the edit page for a listing they authored or administer through an organization.
2. The `listingForm` pack mounts `ListingForm`, reading listing data from the `listingform-data` DOM element's dataset.
3. Because the listing has a non-null `id`, the component renders the edit layout: title input, body markdown textarea, and tags field pre-filled with existing values.
4. Category and expiry-date fields are not shown in the edit view.

### User updates listing fields and submits

1. The user modifies the title (up to 128 characters), body markdown (up to 400 characters), and/or tags using the respective field components.
2. Each change is reflected in `ListingForm` state via `linkState` bindings.
3. The form is submitted to the `PUT /api/v0/listings/:id` or `PUT /api/v1/listings/:id` endpoint.
4. The controller authenticates the user, then calls `set_and_authorize_listing` to load and authorize the target listing.
5. The update action processes the change and returns HTTP 200.

### Policy blocks unauthorized edit attempt

1. A user sends an update request for a listing they did not create and for whose organization they are not an admin.
2. `ListingPolicy#edit?` returns `false` because neither `user_author?` nor `authorized_organization_admin_editor?` is satisfied.
3. The request is rejected with an authorization error.

### Organization admin edits a listing on behalf of the organization

1. A user who is an org admin for the organization that owns the listing navigates to the listing's edit page.
2. `ListingPolicy#edit?` delegates to `authorized_organization_admin_editor?`, which calls `user.org_admin?(record.organization_id)` and returns `true`.
3. The edit form is displayed and the admin can update title, body, and tags.

## Failures / Exceptions

- Submitting an edit without authentication causes the `authenticate_with_api_key_or_current_user!` before-action to reject the request before the listing is loaded.
- If the listing record is not found by `params[:id]`, `Listing.find` raises `ActiveRecord::RecordNotFound`, which the API controller layer handles as a 404 response.
