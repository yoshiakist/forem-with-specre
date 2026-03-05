---
id: "01KJ02CX5937HVK61GE4PHCKAT"
name: "user_can_view_organization_members"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/organizations_controller.rb`
- `app/views/organizations/members.html.erb` (Template)
- `spec/requests/organizations_members_spec.rb` (Test)

## Functional Overview

When a visitor navigates to an organization's members page (identified by the organization's slug), the system looks up the organization and returns its active members. Pending members are excluded. The page is available in two formats: an HTML view that renders a grid of member cards showing each member's avatar, display name, username, and a follow button; and a JSON endpoint that returns a minimal list of member objects containing only id, name, and username. If the organization slug does not match any existing organization, the system returns a 404 response in the appropriate format.

## Scenarios

### Viewing active members as HTML

1. A visitor requests the members page for a valid organization slug via a browser.
2. The system finds the organization by its slug and collects its active (non-pending) members.
3. The system renders an HTML page displaying the organization name with the member count, followed by a responsive grid of member cards.
4. Each card shows the member's avatar (linked to their profile), display name, username, and a follow button.

### Viewing active members as JSON

1. A client requests the members endpoint for a valid organization slug with an `Accept: application/json` header.
2. The system finds the organization by its slug and collects its active (non-pending) members.
3. The system responds with a JSON array where each element contains only the member's `id`, `name`, and `username`.

### Pending members are excluded

1. An organization has both active members (admin or member role) and pending members (invited but not yet confirmed).
2. Any request to the members endpoint returns only active members; pending members do not appear in either the HTML view or the JSON response.

## Failures / Exceptions

- If the organization slug does not match any record, the system returns HTTP 404. For HTML requests it renders the static `public/404.html` file without a layout. For JSON requests it returns `{ "error": "not found", "status": 404 }` with a 404 status code.
