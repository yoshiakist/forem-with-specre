---
id: "01KJ9FWCV9BVZBNN3YJAXS5ZQS"
name: "admin_views_pending_invitations"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/invitations_controller.rb`
- `app/views/admin/invitations/index.html.erb`
- `app/views/admin/users/index/_invitation_actions_dropdown.html.erb`
- `spec/requests/admin/invitations_spec.rb` (Test)

## Functional Overview

When a super-admin navigates to the invitations index page, the system queries all users who have been invited but have not yet registered, applies optional search and role filters, and renders a paginated list of those users. Each entry displays the invited member's username, email address, and the date the invitation was sent. The page provides an overflow-menu dropdown per user with actions to resend or cancel the invitation, and a link to invite additional members. The list is presented in a responsive layout that adapts between small-screen card rows and a large-screen table view.

## Scenarios

### Admin views the list of pending invitations

1. The admin navigates to `/admin/member_manager/invitations`.
2. The system fetches all users in the "invited" state (registered is false), paginated at 50 per page, filtered by any supplied search query or role parameters.
3. The page renders a header titled "Invited Members" with a search form and pagination controls.
4. Each invited user is shown with their username, email address, and the date they were invited (formatted as day, abbreviated month, and year).
5. A per-user dropdown button exposes "Resend" and "Cancel" actions for each invitation.

### Admin searches for a specific invited member

1. The admin enters a search term in the search field and submits the form via GET.
2. The system passes the search parameter to `Admin::UsersQuery`, which filters the invited-user relation accordingly.
3. The page re-renders showing only invited members whose name, email, or username match the query.

### Page shows an empty state when no invitations are pending

1. The admin navigates to the invitations index and no users are in the invited state.
2. The system renders the page with a message "No members invited yet." and a prompt to invite members.
3. A link to create a new invitation is displayed so the admin can act immediately.

### Admin accesses invitation actions via the dropdown

1. The admin clicks the overflow-vertical icon button next to an invited member.
2. A dropdown appears offering two actions: "Resend" (posts to the resend path) and "Cancel" (sends a DELETE request to the invitation path).
3. Selecting "Resend" resubmits the invitation email; selecting "Cancel" removes the pending invitation.

## Design Intent

The controller delegates filtering and search entirely to `Admin::UsersQuery`, keeping the controller action minimal and consistent with other admin user list controllers. Pagination is fixed at 50 per page to limit query cost. The view uses the same `_invitation_actions_dropdown` partial across both the small-screen card layout and the large-screen table layout, passing a `context` parameter so the dropdown button IDs remain unique per row and per layout.
