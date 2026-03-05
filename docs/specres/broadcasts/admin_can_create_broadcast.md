---
id: "01KJ6D4S5MFQG4KCF9VYGRYZW4"
name: "admin_can_create_broadcast"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/broadcasts_controller.rb`
- `app/models/broadcast.rb`
- `app/views/admin/broadcasts/new.html.erb`
- `app/views/admin/broadcasts/_form.html.erb`
- `spec/requests/admin/broadcasts_spec.rb` (Test)
- `spec/models/broadcast_spec.rb` (Test)

## Functional Overview

An admin user can create a new broadcast by submitting a form with a title, HTML content, type (`Welcome` or `Announcement`), an optional banner style, and an active flag. The controller instantiates a `Broadcast` record with the submitted parameters and attempts to save it. On success, the admin is redirected to the broadcast's show page with a success flash message. On failure, the form is re-rendered with validation error messages. Access is restricted to super admins and single-resource admins authorized for `Broadcast`; all other users receive a `Pundit::NotAuthorizedError`.

## Design Intent

The `single_active_announcement_broadcast` model validation enforces a business rule that at most one `Announcement` broadcast may be active at a time, preventing conflicting site-wide announcements. Title uniqueness is scoped to `type_of` so the same title can exist across different broadcast types without conflict.

## Key Members

- `title` — human-readable label for the broadcast; must be unique within each `type_of`
- `processed_html` — HTML content to be displayed to users
- `type_of` — broadcast category; must be `"Welcome"` or `"Announcement"`
- `banner_style` — optional visual style; one of `default`, `brand`, `success`, `warning`, `error`
- `active` — boolean controlling whether the broadcast is currently shown

## Scenarios

### Successful creation by an authorized admin

1. An admin (super admin or Broadcast-scoped single-resource admin) visits the new broadcast page.
2. The admin fills in a title, HTML content, broadcast type, an optional banner style, and sets the active flag.
3. The admin submits the form.
4. The system validates and saves the new `Broadcast` record.
5. The admin is redirected to the broadcast's show page with a success message.

### Unauthorized user is blocked

1. A non-admin user (or a single-resource admin scoped to a different resource) submits a POST request to create a broadcast.
2. The system raises `Pundit::NotAuthorizedError` and the broadcast is not created.

### Validation failure re-renders the form

1. An authorized admin submits the form with missing required fields (e.g., blank title or HTML).
2. The `Broadcast` model fails validation.
3. The controller re-renders the new broadcast form and displays the full error messages as a danger flash.

### Duplicate title within the same type is rejected

1. An authorized admin submits a broadcast with a title and `type_of` combination that already exists.
2. The uniqueness validation fails.
3. The form is re-rendered with an error; the `Broadcast` count does not increase.

### Only one active Announcement broadcast is allowed

1. An authorized admin attempts to create an `Announcement` broadcast with `active: true` while another active `Announcement` broadcast already exists.
2. The `single_active_announcement_broadcast` custom validation fails.
3. The form is re-rendered with an error message; no new record is persisted.

## Failures / Exceptions

- Missing `title`, `type_of`, or `processed_html` causes a presence validation error and re-renders the form.
- A `type_of` value outside `["Announcement", "Welcome"]` is rejected by inclusion validation.
- A `banner_style` value not in `["default", "brand", "success", "warning", "error"]` is rejected (blank is allowed).
- Creating a second active `Announcement` broadcast is blocked by the `single_active_announcement_broadcast` model validation with the message "You can only have one active announcement broadcast".
- Submitting the same title and `type_of` twice creates only one record; the second attempt fails the scoped uniqueness validation.
