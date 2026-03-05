---
id: "01KJ6EAKT3P7HHWCZZXHQ6N8MV"
name: "admin_can_list_and_search_billboards"
status: "draft"
---

## Related Files

- `app/controllers/admin/billboards_controller.rb`
- `app/models/billboard.rb`
- `app/views/admin/billboards/index.html.erb` (Template)
- `app/javascript/packs/admin/billboards.jsx`
- `spec/requests/admin/billboards_spec.rb` (Test)

## Functional Overview

The admin billboards index action allows authorized administrators to view a paginated list of all billboards, ordered by most recently created first, with 50 records per page. When a search term is provided via the `search` query parameter, the list is filtered using the `search_ads` scope on the `Billboard` model, which performs case-insensitive (ILIKE) substring matching against the billboard's name, processed HTML content, and placement area. The index view renders each billboard's name, placement area, display target group, type, published/approved status, and success rate in a table, along with navigation links to create, edit, view details, or destroy each entry.

## Scenarios

### Listing all billboards without a search term

1. An authorized admin navigates to the admin billboards index page.
2. The system fetches all billboards ordered by descending ID and paginates them at 50 per page.
3. The page renders the full list with columns for name, placement area, display group, type, public status, and success rate.
4. Pagination controls appear above and below the table if there are more than 50 records.

### Filtering billboards by keyword search

1. An authorized admin enters a search term in the search field and submits the form.
2. The system passes the `search` parameter to the `search_ads` scope on `Billboard`.
3. The scope filters records whose name, processed HTML, or placement area contains the search term (case-insensitive, partial match).
4. The page re-renders showing only the matching billboards, paginated at 50 per page.

### Non-admin is blocked from the index

1. A user without admin privileges attempts to access the admin billboards index.
2. The system raises a `Pundit::NotAuthorizedError` and denies access.

### Super admin or billboard-scoped single-resource admin accesses the index

1. A super admin or a single-resource admin scoped to `Billboard` navigates to the admin billboards index.
2. The system authorizes the request via `InternalPolicy`.
3. The response is returned with HTTP 200 and the billboard list is displayed.

## Design Intent

The `search_ads` scope uses ILIKE on three columns (name, processed_html, placement_area) to allow admins to find billboards by visible label, content snippet, or location without requiring exact matches. Pagination is fixed at 50 records to keep the page manageable given that billboard counts can grow large. The search form uses GET so that search results are bookmarkable and shareable via URL.
