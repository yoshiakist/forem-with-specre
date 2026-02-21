---
id: "01KJ02MNP5AREF4M1SM48V0ED6"
name: "admin_can_view_organizations"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/organizations_controller.rb`
- `app/helpers/admin/organizations_helper.rb`
- `app/javascript/packs/admin/organizations.jsx`
- `app/javascript/packs/admin/organizations/modals.js`
- `spec/requests/admin/organizations_spec.rb` (Test)
- `spec/helpers/admin/organizations_helper_spec.rb` (Test)
- `spec/system/admin/admin_manages_organizations_spec.rb` (Test)
- `app/views/admin/organizations/index.html.erb` (Template)
- `app/views/admin/organizations/show.html.erb` (Template)
- `app/views/admin/organizations/_activity.html.erb` (Template)

## Functional Overview

An authenticated admin can browse all organizations through a paginated list and drill into an individual organization's detail page. The index page displays each organization's name, ID, Twitter handle, GitHub username, and website URL, and supports name-based search to narrow the list. Clicking an organization navigates to its detail page, which presents the organization's profile (avatar, slug, creation date, member count, contact links), an activity summary (article count and follower count), and the current credit balance. The detail page also surfaces a deletion modal that validates eligibility before allowing a delete action; this modal is rendered client-side via `showOrganizationModal`, which caches hidden HTML content from the page and displays it in a window modal on demand.

## Design Intent

The index deliberately caps results at 50 per page (`PER_PAGE_MAX = 50`) to prevent slow queries over large datasets. When a search term is present, results are filtered by name match rather than sorted by creation date, keeping the search experience focused. On the detail page, the deletion modal content is embedded as hidden HTML and moved into a client-side cache on first access, avoiding duplicate DOM IDs that would arise from Preact's modal duplication strategy.

## Scenarios

### Listing all organizations

1. Admin navigates to the organizations index (`/admin/content_manager/organizations`).
2. The system returns up to 50 organizations ordered by creation date, newest first.
3. The page renders a table with each organization's name (linked to its detail page), ID, Twitter handle, GitHub username, and website URL.
4. Pagination controls appear above and below the table when there are more than 50 results.

### Searching organizations by name

1. Admin types a partial or full organization name into the search field on the index page and submits the form.
2. The system filters the paginated set using a case-insensitive name match (`simple_name_match`) and returns only matching organizations.
3. Non-matching organizations are absent from the result table.

### Viewing a single organization's detail

1. Admin clicks an organization's name link on the index page.
2. The system loads the organization record and renders the detail page.
3. The header shows the organization's avatar, name, slug, ID, creation date, member count, and available contact links (email, GitHub, Twitter).
4. The activity section lists the total number of articles and followers associated with the organization.
5. The current unspent credit balance is shown in the Credits section heading.

### Opening the deletion modal

1. On the organization detail page, the admin clicks the overflow-menu button to reveal the options dropdown.
2. The admin selects "Delete" from the dropdown.
3. `showOrganizationModal` is triggered via a delegated click listener on `document.body`.
4. The function reads the `data-modal-content-selector` attribute on the clicked element (`#delete-organization`) and retrieves the hidden modal HTML, caching it for subsequent opens.
5. The modal is displayed with the title and size specified in the button's data attributes.
6. If the current user is not a super admin, or if the organization still has credits, `deletion_modal_error_message` returns a descriptive error string, and the modal shows that error instead of the delete form.
7. If neither condition applies, the modal presents a delete confirmation form.
