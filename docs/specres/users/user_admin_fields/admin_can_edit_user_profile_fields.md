---
id: "01KJ9N9DR416HTC8Z4EWY5SYMR"
name: "admin_can_edit_user_profile_fields"
status: "in-development"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `spec/requests/admin/users_spec.rb` (Test)

## Functional Overview

An admin can edit a subset of a user's profile fields through the admin panel. The editable fields are split into two groups: user-level fields (`name`, `username`) and profile-level fields (`summary`, `location`, `website_url`). When the admin submits the form, the controller snapshots the current values of all five fields before calling `Users::Update.call` with the submitted params. If the update succeeds, an audit `Note` with reason `admin_profile_update` is created, containing a human-readable description of every field that changed (showing the before and after values). On failure the update errors are surfaced in a flash message. In both cases the admin is redirected back to the user's admin show page.

## Design Intent

Snapshotting previous values before the update, rather than relying on ActiveRecord dirty tracking after the fact, keeps the change-description logic straightforward and independent of whether AR callbacks have already cleared the dirty state. Splitting params into `ADMIN_PROFILE_USER_PARAMS` and `ADMIN_PROFILE_PROFILE_PARAMS` reflects the underlying data model where `name`/`username` live on the `User` record and `summary`/`location`/`website_url` live on the associated `Profile` record. The audit note uses a no-op message when no values actually changed, preserving a complete audit trail even for no-op submissions.

## Key Members

- `ADMIN_PROFILE_USER_PARAMS` — `[:name, :username]`; fields permitted from the `user` param namespace and written to the `User` model
- `ADMIN_PROFILE_PROFILE_PARAMS` — `[:summary, :location, :website_url]`; fields permitted from the `profile` param namespace and written to the `Profile` model
- `Users::Update.call(user, user:, profile:)` — service object that performs the actual persistence; returns a result object with `#success?` and `#errors_as_sentence`
- `profile_update_note` — private helper that compares snapshots to current values and builds a human-readable change summary
- `append_profile_change` — private helper that adds a `"field: 'old' -> 'new'"` entry to the changes list if the value changed

## Scenarios

### Successful profile update with field changes

1. Admin submits the edit-profile form with new values for one or more of `name`, `username`, `summary`, `location`, or `website_url`
2. Controller records the current values of all five fields before making any changes
3. `Users::Update.call` is invoked with the user-level and profile-level params; it succeeds
4. A `Note` record is created linked to the user, with `reason: "admin_profile_update"` and a content string listing every changed field in the form `"field: 'previous' -> 'new'"`; blank values are rendered as `(blank)`
5. A success flash message is set and the admin is redirected to the user's admin show page

### Update fails validation

1. Admin submits the edit-profile form with invalid values (e.g. a username that violates uniqueness or format constraints)
2. Controller records previous values and calls `Users::Update.call`; the service returns a failure result
3. No `Note` is created
4. The validation errors from the service are surfaced as a flash error message (via `errors_as_sentence`)
5. The admin is redirected to the user's admin show page (with the error flash visible)

### Update submitted with no actual changes

1. Admin submits the edit-profile form with values identical to the current stored values
2. `Users::Update.call` succeeds (no-op update)
3. A `Note` is created with the content `"Admin <username> submitted a profile update with no changes detected."`
4. A success flash message is set and the admin is redirected to the user's admin show page

## Failures / Exceptions

- If the user record is not found, `ActiveRecord::RecordNotFound` is raised before reaching the update logic (standard Rails 404 behaviour for the admin panel)
- If the user has no associated `Profile` record, the controller calls `build_profile` to produce an in-memory instance for snapshotting, preventing a nil-reference error when reading profile field values
