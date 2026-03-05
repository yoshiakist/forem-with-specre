---
id: "01KJXY2EH4JHHV5SBS4KPNYYAH"
name: "user_views_reading_list"
status: "draft"
---

## Related Files

- `app/controllers/reading_list_items_controller.rb`
- `app/javascript/packs/readingList.jsx`
- `app/javascript/readingList/readingList.jsx`
- `app/javascript/readingList/components/ItemListItem.jsx`
- `app/javascript/readingList/components/TagList.jsx`
- `app/views/reading_list_items/index.html.erb`
- `spec/requests/reading_list_items_spec.rb` (Test)
- `spec/system/user_views_a_reading_list_spec.rb` (Test)
- `app/javascript/readingList/components/__tests__/ItemListItem.test.jsx` (Test)
- `app/javascript/readingList/__tests__/readingList.test.jsx` (Test)

## Functional Overview

When a user navigates to the reading list page, the application mounts a `ReadingList` Preact component into the `#reading-list` DOM element and a `Snackbar` into the `#snack-zone` element. The `ReadingList` component performs an initial search against the API for bookmarked articles filtered by the current status view (either active or archived), determined by a data attribute on the root element. The user can then filter items by text search or tag, toggle between the active reading list and the archive, archive or unarchive individual items, and load additional pages of results. The component re-mounts on InstantClick page transitions to support client-side navigation.

## Design Intent

The pack file acts as a thin entry point that delegates all rendering and state management to the `ReadingList` component. This separation allows the component to be tested and reused independently of the page-load lifecycle. The `statusView` is passed from a server-rendered data attribute so the same component handles both `/readinglist` and `/readinglist/archive` without separate entry points. InstantClick integration ensures the reading list is re-initialized after soft navigation without a full page reload.

## Key Members

- `statusView: "valid,confirmed" | "archived"` — determines whether the active reading list or the archive is displayed; sourced from `root.dataset.view`
- `availableTags: string[]` — tag list available for filtering; initially empty, populated after the first search
- `selectedTag: string` — the currently active tag filter
- `query: string` — the current free-text search input
- `items: object[]` — the list of reading list items currently displayed
- `itemsTotal: number` — total count of items matching the current filter, shown in the page heading
- `showLoadMoreButton: boolean` — controls whether the "Load more" pagination button is rendered
- `STATUS_VIEW_VALID` — constant `"valid,confirmed"` representing the active reading list view
- `STATUS_VIEW_ARCHIVED` — constant `"archived"` representing the archive view

## Scenarios

### Page loads with active reading list

1. The browser loads `/readinglist` and the server renders a `#reading-list` element with `data-view="valid,confirmed"`.
2. The pack mounts a `Snackbar` into `#snack-zone` and a `ReadingList` with `statusView="valid,confirmed"` into `#reading-list`.
3. The component performs an initial search filtered to status `valid,confirmed` and populates the item list.
4. If a tag was previously persisted in browser state, it is automatically selected and the results are filtered accordingly.
5. The page heading shows "Reading list (N)" where N is the total item count.

### Page loads with archive view

1. The browser loads `/readinglist/archive` and the server renders a `#reading-list` element with `data-view="archived"`.
2. The pack mounts `ReadingList` with `statusView="archived"`.
3. The component performs an initial search filtered to status `archived`.
4. The page heading shows "Archive (N)".

### User filters by text search

1. The user types in the search input field.
2. The component debounces the keystroke and performs a new search with the entered query against the current status view.
3. The item list updates to show only matching results.
4. If no results match, the message "Nothing with this filter" is displayed.

### User filters by tag (desktop)

1. On screens at or above the Medium breakpoint, a sidebar tag list is shown.
2. The user clicks a tag in the tag list.
3. The component selects the tag and re-runs the search filtered to that tag and the current status view.
4. The item list updates to show only items carrying that tag.

### User filters by tag (mobile)

1. On screens below the Medium breakpoint, the tag list appears inline in the header fieldset instead of the sidebar.
2. The user selects a tag; behavior is the same as the desktop scenario.

### User toggles to archive view

1. The user clicks the "View archive" link.
2. The component switches `statusView` to `"archived"`, clears the item list, and re-runs the search.
3. The browser URL is updated to `/readinglist/archive` via `history.replaceState` without a page reload.
4. The page heading changes to "Archive (N)".

### User toggles back to reading list

1. The user clicks the "View reading list" link while in archive view.
2. The component switches `statusView` to `"valid,confirmed"`, clears the item list, and re-runs the search.
3. The browser URL is updated to `/readinglist`.
4. The page heading changes to "Reading list (N)".

### User archives an item

1. The user clicks the "Archive" button on a reading list item.
2. The component sends a PUT request to `/reading_list_items/:id` with the current status.
3. The item is immediately removed from the displayed list and the total count decreases by one.
4. A snackbar notification appears with the message "Archiving...".

### User unarchives an item

1. The user clicks the "Unarchive" button on an archived item.
2. The component sends a PUT request to `/reading_list_items/:id` with the current status.
3. The item is immediately removed from the archive view and the total count decreases by one.
4. A snackbar notification appears with the message "Unarchiving...".

### User loads more items

1. The item list contains a page of results and there are additional items available.
2. A "Load more" button is shown at the bottom of the list.
3. The user clicks "Load more".
4. The next page of results is appended to the existing item list.

### Reading list is empty (no filter)

1. Items are loaded and the result set is empty with no active tag or text filter.
2. The component displays the heading "Your reading list is empty" with a prompt to use the bookmark reaction on a post.

### InstantClick navigation

1. The user navigates to another page and then returns to the reading list via InstantClick (soft navigation).
2. The `change` event fires and `loadElement` is called again.
3. The `ReadingList` and `Snackbar` components are re-mounted into their respective DOM elements.

## Failures / Exceptions

- If the `#reading-list` element is not present in the DOM, `loadElement` exits silently and nothing is rendered.
- If the PUT request to archive or unarchive an item fails, no rollback of the optimistic UI update is performed; the item remains removed from the list.
