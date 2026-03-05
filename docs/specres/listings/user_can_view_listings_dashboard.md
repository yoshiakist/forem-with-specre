---
id: "01KJXW7T67VPX2HZKKWN70MM4E"
name: "user_can_view_listings_dashboard"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/models/listing.rb`
- `app/javascript/listings/listingDashboard.jsx`
- `app/javascript/listings/dashboard/listingRow.jsx`
- `app/javascript/listings/dashboard/rowElements/actionButtons.jsx`
- `app/javascript/listings/dashboard/rowElements/listingDate.jsx`
- `app/javascript/listings/dashboard/rowElements/location.jsx`
- `app/javascript/listings/dashboard/rowElements/tags.jsx`
- `app/javascript/packs/listingDashboard.jsx`
- `app/javascript/listings/__tests__/ListingDashboard.test.jsx` (Test)

## Functional Overview

The listings dashboard presents a user's classified listings in a filterable, sortable interface. On load, the component reads listing data, organizations, and credit counts from the DOM element's data attributes. Users can toggle between their personal listings and per-organization listings using tab-like buttons. Within the active context, listings can be filtered by status (All, Active, Draft, Expired) and sorted by creation date or most-recently-bumped date. Each listing row shows the title (with an "(expired)" suffix when applicable), the bumped or updated date, optional expiry date, optional location, category link, tag links, and action buttons (Edit, Delete, and "View draft" for unpublished listings). The Listing model maps to the `classified_listings` database table.

## Design Intent

Listing state (draft, expired, active) is derived entirely on the client from the `bumped_at` and `published` fields rather than a dedicated status column, keeping the data payload minimal. Data is embedded in the page as JSON data attributes on the root DOM element, avoiding a separate API call on dashboard load.

## Key Members

- `selectedListings` — `'user'` or an organization ID; controls which set of listings is shown
- `filter` — one of `'All'`, `'Active'`, `'Draft'`, `'Expired'`; applied to the displayed listing set
- `sort` — `'created_at'` or `'bumped_at'`; controls the sort order within the displayed listing set
- `isExpired(listing)` — a listing is expired when it has a `bumped_at` date, is not published, and that date is more than 30 days ago
- `isDraft(listing)` — a listing is a draft when it has never been bumped, or it has a `bumped_at` date but is neither expired nor published

## Scenarios

### Viewing personal listings

1. User navigates to the dashboard page; the page embeds listing and credit data as JSON data attributes.
2. The dashboard initializes with the "Personal" scope selected and listings sorted by creation date descending.
3. Each listing row shows the title, date, category, tags, and Edit/Delete action buttons; a "(expired)" suffix is appended to the title of expired listings.
4. The listing count and available personal credit count are displayed in the header.

### Switching to an organization context

1. The header renders a button for each organization the user belongs to, alongside the "Personal" button.
2. User clicks an organization button; that button receives the `active` CSS class and the view switches to show only that organization's listings.
3. The credit count in the header updates to show the organization's unspent credits.

### Filtering listings by status

1. User clicks one of the filter buttons: All, Active, Draft, or Expired.
2. The dashboard re-renders showing only listings matching the selected status; the clicked button receives the `active` CSS class.
3. Clicking "All" removes any filter and shows every listing for the current scope.

### Sorting listings

1. User selects "Recently Bumped" from the sort dropdown (default is "Recently Created").
2. The current listing set re-renders ordered by `bumped_at` descending, with null values sorted last.

### Navigating from a listing row

1. Clicking the listing title navigates to the public listing page (published) or to the edit page (draft).
2. The "Edit" button links to `/listings/:id/edit`; the "Delete" button links to `/listings/:category/:slug/delete_confirm`.
3. For draft listings, a "View draft" button also appears alongside Edit and Delete.
4. Each tag renders as a link to `/listings?t=:tag`; the category renders as a link to `/listings/:category`.

## Failures / Exceptions

- If the `#listings-dashboard` DOM element is absent on the page, the pack entry point skips rendering entirely.
- Listings with a null `bumped_at` sort to the end of the list regardless of the active sort field.
