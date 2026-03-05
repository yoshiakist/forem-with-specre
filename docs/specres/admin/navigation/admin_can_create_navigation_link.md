---
id: "01KJ7HTKMEBPYZWDJCZXPEBWCA"
name: "admin_can_create_navigation_link"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/navigation_links_controller.rb`
- `app/models/navigation_link.rb`
- `app/views/admin/navigation_links/_add_navigation_link_modal.html.erb` (Template)
- `app/views/admin/navigation_links/_form.html.erb` (Template)
- `app/views/async_info/navigation_links.html.erb` (Template)
- `spec/requests/admin/navigation_link_spec.rb` (Test)
- `spec/models/navigation_link_spec.rb` (Test)

## Functional Overview

A super-admin can create a new navigation link by submitting a form with a name, URL, icon (SVG), section placement, display order position, and visibility audience. The `NavigationLinksController#create` action instantiates a `NavigationLink` with the permitted parameters and attempts to save it. On success, a flash success message is set and the admin is redirected back to the navigation links index. On failure, a flash error message containing the validation errors is shown and the admin is redirected to the same index. After any create, update, or destroy, the controller busts both the `navigation_links` Rails cache key and the edge-cached `/async_info/navigation_links` endpoint to keep rendered navigation in sync.

## Key Members

- `name` — required display label for the link
- `url` — required destination URL; accepts absolute (`https://` or `http://`) or relative paths; local-hostname URLs are automatically stripped to relative paths on save
- `icon` — optional SVG string; must begin with `<svg` and may only contain whitespace after the closing tag; falls back to a default SVG from `app/assets/images/link.svg` when blank and no image is uploaded
- `section` — enum with values `default` (0) or `other` (1), controlling sidebar placement
- `position` — integer controlling sort order within a section
- `display_to` — enum with values `all` (0), `logged_in` (1), or `logged_out` (2), controlling which audience sees the link

## Scenarios

### Successful creation

1. A super-admin opens the "Add navigation link" modal on the navigation links admin page.
2. The admin fills in a name, a valid URL, and optionally an SVG icon, section, position, and display audience, then submits the form.
3. The controller saves the new `NavigationLink` record.
4. The `navigation_links` cache and the edge-cached navigation endpoint are both busted.
5. A success flash message including the link name is shown and the admin is redirected to the navigation links index.

### Failed creation due to validation errors

1. A super-admin submits the creation form with missing or invalid fields (e.g., no name, invalid URL, or a non-SVG icon value).
2. The `NavigationLink` record fails validation and is not saved.
3. A flash error message listing the validation errors is shown and the admin is redirected to the navigation links index.

### Icon falls back to default when omitted

1. An admin submits the creation form without providing an icon or an image upload.
2. Before validation, the model sets the icon field to the contents of `app/assets/images/link.svg`.
3. The record is saved with the default icon.

## Failures / Exceptions

- `name` or `url` absent: record is invalid; error flash is rendered.
- `url` format invalid (not `https://`, `http://`, or a relative path): record is invalid.
- `url` with the same `name` already exists (`uniqueness` scoped to `name`): record is invalid.
- `icon` present but does not match the `<svg …>…` regexp: record is invalid.
