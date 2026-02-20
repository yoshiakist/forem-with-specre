---
id: "01KHYB07ABXD2FDW207KP1GHDH"
name: "admin_organization_views_manage_interface"
status: "draft"
last_verified: "2026-02-21"
---

## Related Files

- app/views/admin/organizations/index.html.erb
- app/views/admin/organizations/show.html.erb
- app/views/admin/organizations/_activity.html.erb

## Functional Overview

The admin organization views provide a searchable index listing all organizations with pagination and social links, and a detailed show page for managing individual organizations. The show page includes organization profile display, fully-trusted toggle, credit management (add/remove), baseline score adjustment, activity summary, and a deletion modal with role-based error messaging.

## Scenarios

### Index page lists organizations with search and pagination

1. The page displays a search field that submits a GET request to filter organizations by name.
2. Organizations are rendered in a paginated table showing name (linked to show page), ID, Twitter, GitHub, and URL.
3. Social links display as clickable links when present, or "N/A" when absent.
4. Pagination controls appear above and below the table.

### Show page displays organization profile header

1. The header shows the organization's profile image, name, slug, ID, creation date, and total member count.
2. Email, GitHub, and Twitter links are displayed conditionally based on presence.
3. A "Visit" link opens the public organization profile in a new tab.
4. An options dropdown contains a delete button that triggers a deletion confirmation modal.

### Show page manages fully-trusted setting

1. The fully-trusted section displays a description and a toggle button.
2. Clicking the button submits a PATCH request to flip the fully_trusted boolean.
3. When enabled, a success notice confirms the organization is fully trusted.

### Show page manages organization credits

1. The credits section displays the current unspent credit count.
2. An "Add Org Credits" form accepts a credit amount (1–99,999) and a required reason note.
3. If the organization has credits, a "Remove Org Credits" form accepts an amount (1 to current balance) with a reason.
4. Both forms submit PATCH requests to the update_org_credits endpoint.

### Show page manages baseline score

1. The baseline score section explains that the score is added to every article published under the organization.
2. A form allows updating the score with a minimum value of 0.

### Activity partial summarizes organization metrics

1. The activity section displays the total article count and follower count for the organization.

### Deletion modal validates before confirming

1. The deletion modal calls the helper to generate an error message based on role and credit balance.
2. If an error message exists, it is displayed as a danger notice and no delete form is shown.
3. If no error exists, a delete confirmation form is shown with a JavaScript confirmation prompt.
