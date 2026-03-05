---
id: "01KJ6EHMAWTR3NAEGM1TB30FPJ"
name: "admin_can_edit_billboard"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/billboards_controller.rb`
- `app/models/billboard.rb`
- `app/helpers/billboard_helper.rb`
- `app/javascript/billboard/locations/index.jsx`
- `app/javascript/billboard/locations/templates.jsx`
- `app/javascript/billboard/tags.jsx`
- `app/javascript/packs/admin/billboardEnabledCountries.jsx`
- `app/views/admin/billboards/edit.html.erb` (Template)
- `app/views/admin/billboards/_form.html.erb` (Template)
- `spec/requests/admin/billboards_spec.rb` (Test)
- `spec/models/billboard_spec.rb` (Test)

## Functional Overview

An admin edits an existing billboard by loading it via `GET /admin/customization/billboards/:id/edit` and submitting changes via `PUT /admin/customization/billboards/:id`. The edit form pre-populates all billboard fields — name, body content, placement area, render mode, template, color, display targeting, audience segment, type, published/approved flags, priority, and expiration. On a successful update, the model runs the same before- and after-save callback chain as on create: markdown is re-processed if the body changed, `content_updated_at` is refreshed when content fields change, all hyperlinks in the rendered HTML have the billboard's `bb` parameter appended or updated, and the audience segment is refreshed if stale and relevant fields changed. Two conditional after-save side effects are unique to the update path: if a previously active (approved and published) billboard is taken down by setting either flag to false, event counts are updated asynchronously via `Billboards::DataUpdateWorker` and the billboard's edge-cache surrogate key is purged; if a `feed_first` billboard transitions from inactive to fully active, the home page edge-cache entry is busted. On validation failure the edit form is re-rendered with error messages.

## Design Intent

The update action mirrors the create flow's callback chain deliberately so that any content or state change is always consistently processed — there is no separate "update pipeline." The `being_taken_down?` and `home_feed_first_being_activated?` guards use saved-change introspection rather than a before-save hook so that side effects (async worker, cache purge) only fire once the database write has succeeded, preventing stale cache state from a rolled-back save.

## Key Members

- `billboard_params` — permitted attributes: `organization_id`, `body_markdown`, `placement_area`, `target_geolocations`, `published`, `approved`, `name`, `display_to`, `tag_list`, `type_of`, `color`, `exclude_article_ids`, `audience_segment_id`, `priority`, `browser_context`, `exclude_role_names`, `target_role_names`, `include_subforem_ids`, `render_mode`, `template`, `custom_display_label`, `requires_cookies`, `expires_at`.
- `being_taken_down?` — true only when both `approved` and `published` were true before the save, and at least one of them just changed to false.
- `home_feed_first_being_activated?` — true only when `placement_area` is `feed_first`, both flags are now true, and at least one of them just changed from false.
- `content_updated_at` — refreshed before save when any of `body_markdown`, `name`, `placement_area`, `color`, `template`, or `render_mode` changes.

## Scenarios

### Admin loads the edit form

1. Admin navigates to the edit path for an existing billboard.
2. The controller fetches the billboard by ID and assigns it to the view.
3. The edit template renders the shared form partial pre-populated with the billboard's current data, including a live preview of the processed HTML.
4. The response returns HTTP 200.

### Admin successfully updates a billboard

1. Admin submits the edit form with valid changes (for example, toggling approved to true, changing priority).
2. The controller calls `update` with the permitted params.
3. The model runs before-save callbacks: markdown is re-processed if the body changed; `content_updated_at` is refreshed if any content field changed.
4. The record is saved to the database.
5. After-save callbacks run: links in the processed HTML are updated with the `bb` param; audience segment is refreshed if stale.
6. A success flash message is set and the admin is redirected back to the edit path for the same billboard.

### Update fails validation

1. Admin submits the edit form with invalid data (for example, an already-expired expiration date combined with approved set to true).
2. The model fails validation and the save is rejected.
3. The controller sets a danger flash with the error sentence and re-renders the edit template.

### Active billboard is taken down

1. Admin updates a billboard that was previously both approved and published, setting either `approved` or `published` to false.
2. The record is saved successfully.
3. The `being_taken_down?` guard evaluates to true.
4. `Billboards::DataUpdateWorker` is enqueued asynchronously to update the billboard's aggregated event counts.
5. The billboard's edge-cache surrogate key is purged via `EdgeCache::PurgeByKey`.
6. Admin is redirected to the edit path with a success flash.

### Feed-first billboard is activated

1. Admin updates a `feed_first` billboard that was previously not fully active, setting both `approved` and `published` to true (one or both having just changed).
2. The record is saved successfully.
3. The `home_feed_first_being_activated?` guard evaluates to true.
4. The home page edge-cache entry (`main_app_home_page`) is purged via `EdgeCache::PurgeByKey` with fallback path `/`.
5. Admin is redirected to the edit path with a success flash.

## Failures / Exceptions

- Submitting `approved: true` with `expires_at` in the past fails with "cannot be set to true if billboard has expired".
- Submitting a `placement_area` not in `ALLOWED_PLACEMENT_AREAS` fails with a presence/inclusion error.
- A `community` type billboard without an `organization_id` fails validation.
- Invalid geolocation codes (not in enabled targets) fail with a descriptive error per invalid code.
- More than 25 tags, tags longer than 30 characters, or non-alphanumeric tags fail validation.
