---
id: "01KJ7HV1S7SD97H4R894DP7Y53"
name: "admin_can_edit_navigation_link"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/navigation_links_controller.rb`
- `app/models/navigation_link.rb`
- `app/views/admin/navigation_links/_edit_navigation_link_modal.html.erb` (Template)
- `app/views/admin/navigation_links/_form.html.erb` (Template)
- `app/views/async_info/navigation_links.html.erb` (Template)
- `spec/requests/admin/navigation_link_spec.rb` (Test)
- `spec/models/navigation_link_spec.rb` (Test)

## Functional Overview

An authenticated admin can update an existing navigation link by submitting a PUT request to the update action with any combination of the permitted fields: name, url, icon, display_to, position, and section. The controller finds the record by ID, applies the permitted parameters, and redirects back to the navigation links index page regardless of outcome, setting a success or error flash message accordingly. After a successful update, the controller busts both the release-tied content fragment cache and the navigation links edge cache so that the rendered sidebar reflects the new values immediately.

## Design Intent

The cache-busting callbacks are registered as `after_action` hooks on create, update, and destroy so that any mutation to navigation links always clears both the Rails cache key `"navigation_links"` and the CDN-level edge cache for the async endpoint. This avoids stale navigation menus being served after admin edits.

## Key Members

- `ALLOWED_PARAMS` — strong-parameter allowlist: `name`, `url`, `icon`, `display_to`, `position`, `section`
- `section` enum — `default` (0) or `other` (1), stored with `_suffix` predicate helpers (e.g., `other_section?`)
- `display_to` enum — `all` (0), `logged_in` (1), `logged_out` (2), stored with `_prefix` predicate helpers

## Scenarios

### Successful field update

1. Admin submits a PUT request to `/admin/customization/navigation_links/:id` with one or more permitted fields.
2. The controller locates the navigation link by ID and applies the new values.
3. Model validations pass; the record is persisted.
4. A success flash message is set using the link's name.
5. The navigation links Rails cache entry and the CDN edge cache for `/async_info/navigation_links` are cleared.
6. The admin is redirected to the navigation links index page.

### Updating the section field

1. Admin submits a PUT request with `section: "other"` for an existing link.
2. The controller updates the record; the link's `other_section?` predicate returns `true`.
3. The caches are busted and the admin is redirected to the index.

### Failed update due to validation error

1. Admin submits a PUT request with invalid field values (e.g., a malformed URL or an icon that does not match the SVG format).
2. Model validation fails; the record is not persisted.
3. An error flash message is set with the validation error sentence.
4. The admin is redirected back to the navigation links index page.

## Failures / Exceptions

- If the navigation link record cannot be found by the given ID, Rails raises `ActiveRecord::RecordNotFound` (no explicit rescue; standard 404 handling applies).
- If model validation fails (missing name/url, invalid URL scheme, icon not matching SVG regexp), the controller sets a flash error with `errors_as_sentence` and redirects without persisting changes.
