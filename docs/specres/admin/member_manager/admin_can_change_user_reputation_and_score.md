---
id: "01KJ9N68RRPC8HY6VF56W9AA9G"
name: "admin_can_change_user_reputation_and_score"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `spec/requests/admin/users/users_change_reputation_modifier_spec.rb` (Test)
- `spec/requests/admin/users/users_change_max_score_spec.rb` (Test)

## Functional Overview

An admin can adjust two numeric scoring fields on any user account: `reputation_modifier` and `max_score`. For each field the admin submits the new value and an optional free-text reason. The system validates the value against the model, updates the user record, and immediately records a `Note` that captures both the new value and the reason. On success a flash success message is displayed and the admin is redirected to the user's admin profile page. On failure the record is not modified, an audit note is not created, a flash error message is displayed, and the admin is redirected to the same page.

## Design Intent

Separating these two actions from the general `update` action keeps each change auditable in isolation. Embedding the reason directly in the note content (rather than a separate field) ensures that even a plain-text log reader can understand what changed and why without joining tables. Routing both through the same `Note` model with distinct `reason` values (`reputation_modifier_change` / `max_score_change`) allows queries to filter by change type.

## Key Members

- `reputation_modifier` — a floating-point multiplier applied to the user's reputation score; model validation rejects values outside an allowed range (values above 5 are invalid)
- `max_score` — an integer ceiling for the user's score; model validation rejects negative values
- `new_note` (optional param) — admin-supplied reason text; when present it is appended to the audit note content as `Reason: <text>`
- `Note#reason` — set to `"reputation_modifier_change"` or `"max_score_change"` to identify the type of administrative action

## Scenarios

### Change reputation modifier with an optional note

1. Admin submits a PATCH request to `reputation_modifier_admin_user_path` with a valid `reputation_modifier` value and a non-empty `new_note`.
2. System validates and saves the new `reputation_modifier` on the user record.
3. System creates a `Note` authored by the current admin with `reason: "reputation_modifier_change"` and content of the form `"Changed user's reputation modifier to <value>. Reason: <note>"`.
4. System sets a flash success message and redirects to the user's admin profile page.

### Change reputation modifier without a note

1. Admin submits a PATCH request to `reputation_modifier_admin_user_path` with a valid `reputation_modifier` value and an empty or absent `new_note`.
2. System validates and saves the new `reputation_modifier` on the user record.
3. System creates a `Note` with `reason: "reputation_modifier_change"` and content of the form `"Changed user's reputation modifier to <value>."` (no reason suffix).
4. System sets a flash success message and redirects to the user's admin profile page.

### Change max score with an optional note

1. Admin submits a PATCH request to `max_score_admin_user_path` with a valid `max_score` value and a non-empty `new_note`.
2. System validates and saves the new `max_score` on the user record.
3. System creates a `Note` authored by the current admin with `reason: "max_score_change"` and content of the form `"Changed user's maximum score to <value>. Reason: <note>"`.
4. System sets a flash success message and redirects to the user's admin profile page.

### Change max score without a note

1. Admin submits a PATCH request to `max_score_admin_user_path` with a valid `max_score` value and an empty or absent `new_note`.
2. System validates and saves the new `max_score` on the user record.
3. System creates a `Note` with `reason: "max_score_change"` and content of the form `"Changed user's maximum score to <value>."` (no reason suffix).
4. System sets a flash success message and redirects to the user's admin profile page.

## Failures / Exceptions

- If the submitted `reputation_modifier` value fails model validation (e.g., value greater than 5), the user record is not updated, no `Note` is created, a flash error message is set, and the admin is redirected to the user's admin profile page.
- If the submitted `max_score` value fails model validation (e.g., a negative number), the user record is not updated, no `Note` is created, a flash error message is set, and the admin is redirected to the user's admin profile page.
