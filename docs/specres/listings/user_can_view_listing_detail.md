---
id: "01KJXWBCMHBTSTY8EW25W3B4CV"
name: "user_can_view_listing_detail"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/models/listing.rb`
- `app/controllers/concerns/api/listings_controller.rb`
- `app/controllers/api/v0/listings_controller.rb`
- `app/controllers/api/v1/listings_controller.rb`
- `app/javascript/listings/listings.jsx`
- `app/javascript/listings/components/Modal.jsx`
- `app/javascript/listings/components/ModalBackground.jsx`
- `app/javascript/listings/singleListing/SingleListing.jsx`
- `app/javascript/listings/singleListing/Header.jsx`
- `app/javascript/listings/singleListing/AuthorInfo.jsx`
- `app/javascript/listings/singleListing/TagLinks.jsx`
- `app/javascript/listings/singleListing/DropdownMenu.jsx`
- `app/javascript/listings/singleListing/listingPropTypes.js`
- `app/views/api/v0/shared/_listing.json.jbuilder`
- `app/views/api/v1/shared/_listing.json.jbuilder`
- `app/javascript/listings/__tests__/Modal.test.jsx` (Test)
- `app/javascript/listings/__tests__/ModalBackground.test.jsx` (Test)
- `app/javascript/listings/__tests__/SingleListing.test.jsx` (Test)

## Functional Overview

When a user clicks on a listing in the listing index, the frontend opens a detail view of that listing without navigating away from the page. The `Listings` root component tracks which listing is currently open (`openedListing`) and whether the modal is visible (`isModalOpen`). If a listing is active, a `Modal` overlay is rendered, which wraps a `SingleListing` component in its expanded ("modal") layout. `SingleListing` composes a `Header` (title link, publication date, `TagLinks`, and `DropdownMenu`), the processed HTML body, and an `AuthorInfo` section (avatar, name, category, optional location). The browser URL is updated to `/listings/:category/:slug` without a full navigation so the detail view is directly shareable. Closing the modal restores the previous URL and clears the opened listing from state. Listings can also be rendered inline on the index page (non-modal mode) with the same `SingleListing` component but without the `Modal` wrapper.

## Design Intent

The modal pattern allows the user to inspect a listing and immediately navigate back to the full list without losing scroll position or filter state. Updating `window.history` with `replaceState` makes the URL shareable while avoiding a full-page load. The `SingleListing` component is reused for both modal and inline display, driven by the `isOpen` prop, so detailed listing rendering logic is not duplicated.

## Key Members

- `openedListing` — the currently selected listing object held in `Listings` state; `null` when no detail view is open.
- `isModalOpen` — boolean flag in `Listings` state that gates rendering of the `Modal` component.
- `isOpen` prop on `SingleListing` — when `true`, renders the modal layout (no card shadow); when `false`, renders the inline card layout.
- `listingPropTypes` — shared PropTypes shape defining the listing data contract: `id`, `category`, `slug`, `title`, `processed_html`, `user_id`, `tag_list`, `author` (with `name`, `username`, `profile_image_90`), and optional `location`.

## Scenarios

### Opening a listing detail view

1. User clicks the title link of a listing card in the index.
2. The `handleOpenModal` handler fires, storing the listing in `openedListing` and setting `isModalOpen` to `true`.
3. The browser URL is updated to `/listings/:category/:slug` via `replaceState`.
4. The `Modal` overlay renders with a `SingleListing` in expanded layout, showing the title, publication date, tags, dropdown menu, processed HTML body, and author info.

### Viewing listing details at a direct URL

1. The server embeds the target listing in the page's data attributes (`data-displayedlisting`).
2. On component mount, the frontend detects the embedded listing, sets it as `openedListing`, and opens the modal immediately.
3. The user sees the listing detail without having clicked a listing card.

### Closing the modal

1. User clicks outside the modal, triggers the close button, or navigates to a tag or category link.
2. `handleCloseModal` clears `openedListing` and sets `isModalOpen` to `false`.
3. The browser URL reverts to the listing index path with current query parameters.

### Interacting with listing metadata

1. User clicks a tag in `TagLinks`; the tag is added to the active filter and the modal closes.
2. User clicks the category link in `AuthorInfo`; the category filter activates and the modal closes.
3. User clicks the author name or avatar; the browser navigates to the author's profile page.

### Dropdown actions for listing owner vs. visitor

1. The `DropdownMenu` compares `currentUserId` with `listing.user_id`.
2. If the current user owns the listing, an "Edit" link to `/listings/:id/edit` is shown.
3. Otherwise, a "Report Abuse" link pointing to the report URL is shown.

## Failures / Exceptions

- If `openedListing` is `null` or `isModalOpen` is `false`, the `Modal` component is not rendered at all (guarded by `shouldRenderModal`).
- If the listing has no `bumped_at` timestamp, the `Header` falls back to `originally_published_at` for the displayed date.
- If the listing has no tags, `TagLinks` renders nothing rather than an empty list.
- If the listing has no `location`, `AuthorInfo` omits the location text entirely.
