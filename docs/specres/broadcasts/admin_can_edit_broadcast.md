---
id: "01KJ6D5ARD28YYPJ5J3T4XPXDS"
name: "admin_can_edit_broadcast"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/broadcasts_controller.rb`
- `app/models/broadcast.rb`
- `app/views/admin/broadcasts/edit.html.erb`
- `app/views/admin/broadcasts/_form.html.erb`
- `spec/requests/admin/broadcasts_spec.rb` (Test)

## Functional Overview

A super-admin can edit an existing broadcast by navigating to its edit page, modifying fields such as title, HTML content, type, banner style, and active status, and submitting the form. The controller locates the broadcast by ID, applies the permitted parameters, and on success redirects to the broadcast's show page with a success flash. If validation fails the edit form is re-rendered with an error flash. Changing the `active` field automatically records an `active_status_updated_at` timestamp on the model before saving.

## Design Intent

Only one `Announcement`-type broadcast may be active at a time. This constraint is enforced at the model level via a custom validation, keeping the controller thin and the rule co-located with the data. Tracking `active_status_updated_at` on every `active` toggle gives operators a precise audit trail without needing a separate audit table.

## Key Members

- `title` — human-readable label; must be unique within the same `type_of`
- `processed_html` — the rendered HTML content delivered to users
- `type_of` — broadcast category; one of `Welcome` or `Announcement`
- `banner_style` — optional visual style; one of `default`, `brand`, `success`, `warning`, `error`
- `active` — whether the broadcast is currently live
- `active_status_updated_at` — timestamp set automatically whenever `active` changes

## Scenarios

### Admin opens the edit form

1. A super-admin navigates to the edit page for an existing broadcast.
2. The system loads the broadcast by its ID and renders the edit form pre-populated with the current field values.

### Admin successfully updates a broadcast

1. The admin modifies one or more fields (title, HTML, type, banner style, active status) and submits the form.
2. The system validates the changes, saves the broadcast, and redirects to the broadcast's show page with a success notice.
3. If the `active` field changed, `active_status_updated_at` is set to the current time.

### Admin activates a broadcast and timestamp is recorded

1. The admin sets `active` to `true` on a broadcast that was previously inactive and submits the form.
2. The system saves the record and updates `active_status_updated_at` to reflect the exact time of the change.
3. The admin is redirected to the show page with a success notice.

### Admin submits invalid data

1. The admin submits the form with data that violates a model validation (e.g., a duplicate title within the same type, or attempting to activate a second `Announcement` broadcast when one is already active).
2. The system re-renders the edit form and displays the validation error messages.

## Failures / Exceptions

- If validation fails (duplicate title within `type_of`, blank required fields, invalid `type_of` or `banner_style` value, or more than one active `Announcement` broadcast), the edit form is re-rendered with the error messages in a danger flash.
- If the broadcast ID does not exist, the controller raises `ActiveRecord::RecordNotFound` (resulting in a 404 response via Rails' default error handling).
