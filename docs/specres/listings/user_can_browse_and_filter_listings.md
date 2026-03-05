---
id: "01KJXWC077QF4CMYHXFFQ278TR"
name: "user_can_browse_and_filter_listings"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/models/listing.rb`
- `app/controllers/concerns/api/listings_controller.rb`
- `app/controllers/api/v0/listings_controller.rb`
- `app/controllers/api/v1/listings_controller.rb`
- `app/javascript/listings/listings.jsx`
- `app/javascript/listings/utils.js`
- `app/javascript/listings/components/AllListings.jsx`
- `app/javascript/listings/components/ListingFilters.jsx`
- `app/javascript/listings/components/ListingFiltersCategories.jsx`
- `app/javascript/listings/components/ListingFiltersTags.jsx`
- `app/javascript/listings/components/CategoryLinks.jsx`
- `app/javascript/listings/components/CategoryLinksMobile.jsx`
- `app/javascript/listings/components/ClearQueryButton.jsx`
- `app/javascript/listings/components/SelectedTags.jsx`
- `app/javascript/listings/components/NextPageButton.jsx`
- `app/javascript/packs/listings.jsx`
- `app/views/api/v0/shared/_listing.json.jbuilder`
- `app/views/api/v1/shared/_listing.json.jbuilder`
- `app/javascript/listings/__tests__/AllListings.test.jsx` (Test)
- `app/javascript/listings/__tests__/Categories.test.jsx` (Test)
- `app/javascript/listings/__tests__/ClearQueryButton.test.jsx` (Test)
- `app/javascript/listings/__tests__/ListingFiltersCategories.test.jsx` (Test)
- `app/javascript/listings/__tests__/ListingFilterTags.test.jsx` (Test)
- `app/javascript/listings/__tests__/NextPageButton.test.jsx` (Test)
- `app/javascript/listings/__tests__/SelectedTags.test.jsx` (Test)
- `app/javascript/listings/__tests__/utils.test.js` (Test)

## Functional Overview

The listings browse and filter feature renders a paginated, filterable index of classified listings in a two-column layout. On page load the `Listings` Preact component reads URL query parameters (`q` for text, `t` for tags, and a category path segment) to restore filter state, then immediately fires a search against the `/search/listings` endpoint. Users can narrow results by typing into a text search field (debounced at 150 ms), selecting one or more tag pills, and choosing a category from a sidebar link list (desktop) or a native select dropdown (mobile). Each combination of active filters updates the browser URL via `history.replaceState` without a full navigation. When a result page is exactly `LISTING_PAGE_SIZE` (75) items the "Load more" button is shown; clicking it increments the page counter and appends the next page of results. Only listings that have a `bumped_at` timestamp are displayed after each API response.

## Key Members

- `LISTING_PAGE_SIZE: 75` — maximum results returned per page; controls whether the next-page button is shown
- `tag_boolean_mode: 'all'` — all selected tags must match (AND logic)
- `page` — zero-based page counter, reset to 0 whenever any filter changes

## Scenarios

### Browsing all listings on page load

1. The page mounts and reads `data-listings`, `data-category`, and `data-allcategories` attributes from the container element.
2. When no query or tags are present in the URL, the server-rendered listings are used directly without an extra API call.
3. The component fires a search anyway so the UI state is fully synchronized with the URL.
4. Listings without a `bumped_at` value are filtered out before display.

### Filtering by text search

1. User types in the search input; input events are debounced at 150 ms.
2. The `Listings` component resets the page to 0 and calls the search API with the current query, tags, and category.
3. The browser URL is updated to include `?q=<query>` without reloading the page.
4. When the query is non-empty a clear button appears; clicking it empties the field and repeats the search.

### Filtering by tag

1. User clicks a tag link on a listing card; the tag is added to the active tags list if not already present.
2. The page is reset to 0 and the search API is called with `tag_boolean_mode: 'all'`, requiring all active tags to match.
3. Active tags appear as removable pills above the search field; clicking the `×` on a pill removes that tag and re-runs the search.
4. The URL is updated to include `?t=<tag1>,<tag2>`.

### Filtering by category

1. User clicks a category link in the sidebar (desktop) or selects from the dropdown (mobile).
2. The `Listings` component sets the new category, resets the page to 0, and calls the search API.
3. The browser URL is updated to `/listings/<category>` (optionally with query/tag parameters appended).
4. The selected category link receives the `crayons-link--current` style and a `data-testid="selected-category"` attribute; the "All listings" link is highlighted only when no category is active.

### Loading more results

1. After a search returns exactly 75 results, the "Load more..." button is rendered below the listing grid.
2. User clicks the button; the page counter increments by 1 and the search API is called with the same filters.
3. The new page of results replaces the current listing grid.
4. If the new page returns fewer than 75 results, the "Load more..." button is hidden.

## Failures / Exceptions

- Listings without a `bumped_at` field are silently excluded from the rendered grid by `updateListings`.
- The masonry grid layout recalculates row spans on every update and on window resize to prevent content overflow.
