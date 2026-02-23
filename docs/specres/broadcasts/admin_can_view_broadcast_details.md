---
id: "01KJ6D7FQ3E8XSXDJQS2EYZTJ8"
name: "admin_can_view_broadcast_details"
status: "draft"
---

## Related Files

- `app/controllers/admin/broadcasts_controller.rb`
- `app/helpers/broadcasts_helper.rb`
- `app/views/admin/broadcasts/show.html.erb`
- `spec/requests/admin/broadcasts_spec.rb` (Test)

## Functional Overview

When an admin navigates to a broadcast's detail page, the system looks up the broadcast by ID and renders a show view presenting its title, type, processed HTML content, active/inactive status, last active timestamp, and an HTML preview of the broadcast. The page also provides Edit and Destroy actions. The Destroy action is gated behind a confirmation modal before proceeding. A banner preview is rendered using a helper that computes the appropriate CSS class based on the broadcast's `banner_style` attribute.

## Design Intent

The show action is intentionally minimal — it delegates all display logic to the view and a helper. The `banner_class` helper centralises banner CSS class computation so that both the admin preview and any other consumer can rely on a consistent rendering contract. Sanitizing the `processed_html` output in the preview (allowing only `href`, `style`, and `src` attributes) limits XSS exposure while still permitting the visual preview to be meaningful.

## Key Members

- `@broadcast` — the `Broadcast` record fetched by `params[:id]`; provides `title`, `type_of`, `processed_html`, `active_status_updated_at`, `active?`, `banner_style`, and `id`
- `banner_class(broadcast)` — returns a CSS class string derived from `banner_style`; returns `nil` when `banner_style` is blank
- `sanitized_broadcast_id(broadcast_title)` — returns a CSS-safe identifier by downcasing, removing colons, and replacing spaces with underscores

## Scenarios

### Admin views a broadcast's detail page

1. An authenticated admin visits the detail URL for a specific broadcast.
2. The system fetches the broadcast record by its ID.
3. The page renders the broadcast's title, type, content (processed HTML), active/inactive status badge, and the last time the active status was changed.
4. If the broadcast has processed HTML content, an HTML preview section is shown, styled with the appropriate banner CSS class.

### Admin sees active status indicated visually

1. When the broadcast is active, a green "Active" indicator is shown.
2. When the broadcast is inactive, a yellow "Inactive" indicator is shown.

### Admin initiates a destroy from the detail page

1. The admin clicks the Destroy button on the detail page.
2. A confirmation modal opens, asking the admin to confirm before the broadcast is deleted.
3. On confirmation, the destroy request is sent to the broadcasts endpoint.

### Admin navigates to edit from the detail page

1. The admin clicks the Edit button on the detail page.
2. The system redirects the admin to the edit form for that broadcast.

## Failures / Exceptions

- If the broadcast ID does not correspond to an existing record, `Broadcast.find` raises `ActiveRecord::RecordNotFound`, which the application handles with a standard 404 response.
