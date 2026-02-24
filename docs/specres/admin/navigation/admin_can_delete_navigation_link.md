---
id: "01KJ7HVCMVN775VM9T710ABMRW"
name: "admin_can_delete_navigation_link"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/navigation_links_controller.rb`
- `app/models/navigation_link.rb`
- `spec/requests/admin/navigation_link_spec.rb` (Test)
- `app/views/admin/navigation_links/index.html.erb` (Template)
- `app/views/async_info/navigation_links.html.erb` (Template)

## Functional Overview

An admin can permanently delete a navigation link by submitting a DELETE request to the admin navigation links endpoint. The system looks up the link by ID, destroys it, and on success sets a localized flash message and redirects back to the navigation links index page. If destruction fails, an error flash message is shown instead. After any mutation, the system automatically busts the navigation links Rails cache entry and the CDN edge cache for the async navigation links endpoint, ensuring all subsequent requests reflect the updated link set.

## Design Intent

Cache-busting is performed as an `after_action` callback shared with create and update so that any mutation (including deletion) always produces a fresh navigation-link payload for both server-rendered and edge-cached clients. This avoids stale menus appearing to end users after an admin removes a link.

## Scenarios

### Successful deletion

1. Admin sends a DELETE request for an existing navigation link identified by its ID.
2. The system finds the navigation link record and destroys it.
3. A localized success flash message referencing the link's name is set.
4. The Rails cache entry for navigation links is invalidated and the CDN edge cache for the async navigation links path is busted.
5. The admin is redirected to the navigation links index page.

### Redirect to index after deletion

1. Admin sends a DELETE request for an existing navigation link.
2. The system processes the deletion and redirects to the navigation links index path regardless of outcome.

### Navigation link count decreases

1. Admin sends a DELETE request for an existing navigation link.
2. The total count of navigation links in the database decreases by one.

## Failures / Exceptions

- If the navigation link cannot be destroyed (e.g., validation or callback prevents it), an error flash message containing the record's error sentences is set, and the admin is still redirected to the index page.
