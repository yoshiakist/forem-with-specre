---
id: "01KJ0295AV619CEC61P9EVC0V8"
name: "user_can_update_organization_settings"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/organizations_controller.rb`
- `app/models/organization.rb`
- `app/services/edge_cache/bust_organization.rb`
- `app/workers/organizations/bust_cache_worker.rb`
- `spec/requests/organizations_update_spec.rb` (Test)
- `spec/services/edge_cache/bust_organization_spec.rb` (Test)
- `spec/workers/organizations/bust_cache_worker_spec.rb` (Test)

## Functional Overview

An organization admin submits updated settings — such as display name, colors, social links, or profile image — via a `PUT /organizations/:id` request. The controller validates the profile image when one is provided, then persists the changes and stamps `profile_updated_at` to the current time. All member users have their `organization_info_updated_at` touched so that cached user data remains fresh. After a successful save the model triggers `Organizations::BustCacheWorker` asynchronously, which calls `EdgeCache::BustOrganization` to purge cached pages for the organization's profile path and all of its associated articles. On failure the edit form is re-rendered with validation errors. A separate `generate_new_secret` action allows an admin to rotate the organization's invitation secret at any time.

## Design Intent

Touching `organization_info_updated_at` on every member after an update ensures that any per-user caches embedding organization data are invalidated without requiring an explicit cache key per user. Delegating cache-busting to a background worker (`Organizations::BustCacheWorker`) keeps the request cycle short even when the organization has many articles to purge.

## Key Members

- `ORGANIZATIONS_PERMITTED_PARAMS` — allowlist of field names accepted from the update form, covering profile, branding, social, and CTA fields
- `profile_updated_at` — timestamp stamped to `Time.current` on every successful update, separate from the model's built-in `updated_at`
- `organization_info_updated_at` — timestamp on each member user record, touched in bulk after a successful organization update

## Scenarios

### Successful settings update

1. An authenticated admin submits a `PUT /organizations/:id` request with one or more permitted fields.
2. The controller calls `set_organization`, which looks up the record by id and authorizes the current user.
3. If a profile image is included, the controller validates that it is a real file and that its filename does not exceed the length limit; the request is re-rendered with an error and halted if either check fails.
4. The organization record is updated with the permitted params merged with `profile_updated_at: Time.current`.
5. All users belonging to the organization have their `organization_info_updated_at` touched.
6. A success notice is set and the user is redirected to `/settings/organization`.
7. The model's `after_save` callback enqueues `Organizations::BustCacheWorker` with the organization's id and slug.

### Failed settings update (validation errors)

1. An authenticated admin submits a `PUT /organizations/:id` request with invalid field values (e.g., a color hex that does not match `COLOR_HEX_REGEXP`, or a name that exceeds 50 characters).
2. The `Organization#update` call returns false.
3. The controller loads the organization's memberships to populate the edit form.
4. The edit form (`users/edit` template) is re-rendered with the validation errors displayed.

### Profile image rejected

1. An admin submits a `PUT /organizations/:id` request that includes a profile image parameter.
2. The controller's `valid_image?` check determines the value is not an actual uploaded file, or that the filename exceeds the permitted length.
3. The controller halts before attempting to save and re-renders the edit form with the appropriate error on `:profile_image`.

### Organization not found

1. An admin submits a `PUT /organizations/:id` request where the id does not correspond to any organization record.
2. `set_organization` calls `Organization.find_by(id: ...)` and receives nil.
3. The controller raises `ActiveRecord::RecordNotFound` (via `not_found`), resulting in a 404 response.

### Admin rotates organization secret

1. An authenticated admin submits a `POST /organizations/generate_new_secret` request with the organization id.
2. The controller calls `set_organization` to load and authorize the record.
3. A new random 100-character hex secret is generated via `Organization#generated_random_secret` and assigned.
4. The record is saved, a success notice is set, and the admin is redirected to the organization settings page.

## Failures / Exceptions

- If the profile image parameter is a plain string rather than an uploaded file object, `valid_image_file?` adds an `invalid file type` error to the organization and the update is aborted.
- If the profile image filename exceeds the permitted length, `valid_filename?` adds a `filename too long` error and the update is aborted.
- If the organization id in the request does not match any record, `not_found` is called, raising `ActiveRecord::RecordNotFound`.
- `EdgeCache::BustOrganization` rescues `StandardError` when iterating over articles to bust, logging the error rather than propagating it, so a cache-bust failure does not surface to the user.
- `Organizations::BustCacheWorker` returns early without calling `EdgeCache::BustOrganization` if either `organization_id` or `slug` is nil, or if the organization record cannot be found.
