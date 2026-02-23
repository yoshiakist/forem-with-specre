---
id: "01KJ6D3VR5PTRXZFBE5SVTSYM1"
name: "admin_can_list_broadcasts"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/broadcasts_controller.rb`
- `app/models/broadcast.rb`
- `app/views/admin/broadcasts/index.html.erb`
- `spec/requests/admin/broadcasts_spec.rb` (Test)

## Functional Overview

When an authorized admin visits the broadcasts index, the system retrieves all broadcasts from the database ordered alphabetically by title. If a `type_of` query parameter is provided, the list is filtered to only broadcasts matching that type (e.g., "Announcement" or "Welcome"). The resulting list is rendered in a table view that shows each broadcast's title as a link and an active/inactive status indicator. The page also provides type-based navigation tabs and a button to create a new broadcast. Access is restricted to admins with explicit Broadcast resource permission; non-admins and admins scoped to other resources receive a `Pundit::NotAuthorizedError`.

## Scenarios

### Super admin views all broadcasts

1. A super admin navigates to the broadcasts index without any type filter.
2. The system loads all broadcasts, sorted by title ascending.
3. The page renders a table listing every broadcast with its title and active/inactive status.

### Admin filters broadcasts by type

1. A super admin navigates to the broadcasts index with a `type_of` query parameter (e.g., "announcement" or "welcome").
2. The system capitalizes the parameter value and queries for broadcasts matching that type.
3. The page renders only broadcasts of the requested type, sorted by title.

### Single-resource admin for Broadcast accesses the list

1. A user with single-resource admin rights scoped to `Broadcast` navigates to the broadcasts index.
2. The authorization check passes because the user has the required resource permission.
3. The system returns a 200 OK response with the broadcasts list.

### Non-admin is blocked from the broadcasts index

1. A regular user (non-admin) attempts to access the broadcasts index.
2. The authorization policy raises `Pundit::NotAuthorizedError`.
3. The request does not complete and no broadcast data is returned.

### Wrong single-resource admin is blocked

1. A user with single-resource admin rights scoped to a different resource (e.g., `Article`) attempts to access the broadcasts index.
2. The authorization policy raises `Pundit::NotAuthorizedError` because the resource scope does not match `Broadcast`.

## Failures / Exceptions

- Any request from a non-admin user raises `Pundit::NotAuthorizedError` via `InternalPolicy`.
- A single-resource admin scoped to a resource other than `Broadcast` is also denied with `Pundit::NotAuthorizedError`.
