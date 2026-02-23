---
id: "01KJ6EH2F7D1Q61H1A07JXRE38"
name: "admin_can_create_billboard"
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
- `app/views/admin/billboards/new.html.erb` (Template)
- `app/views/admin/billboards/_form.html.erb` (Template)
- `spec/requests/admin/billboards_spec.rb` (Test)
- `spec/views/admin/billboards/new_spec.rb` (Test)
- `spec/models/billboard_spec.rb` (Test)

## Functional Overview

An admin visits the new billboard form, fills in targeting options — placement area (required), body markdown content (required), render mode, template style, optional border color, display audience (all / logged-in / logged-out), optional audience segment, browser context, geolocation targets, tag list, ad type (in-house / community / external), organization ID, publication/approval flags, priority flag, and expiration date — then submits the form. On a valid submission the controller saves the record, assigns the current user as creator, and redirects to the edit page with a success flash. Before saving the model renders the body markdown into `processed_html` and records `content_updated_at`; after saving it auto-generates a name when none was provided, appends a `bb` tracking parameter to every link in `processed_html`, and asynchronously refreshes a stale audience segment when applicable.

## Design Intent

The creator is set explicitly in the controller (not derived from the form params) so that the billboard always has an authenticated audit trail regardless of what params are submitted. Auto-naming (`Billboard <id>`) ensures records are never unnamed even when the admin leaves the field blank. The `bb` param tracking is applied as an `after_save` callback so that the record ID is available at the time of URL rewriting.

## Key Members

- `placement_area` — one of `ALLOWED_PLACEMENT_AREAS`; determines where the ad is rendered and the image prefix width (350 px for sidebar, 775 px otherwise)
- `body_markdown` / `processed_html` — source and rendered HTML; `render_mode` controls whether the body is processed as Forem markdown or passed through as raw HTML
- `display_to` — enum: `all`, `logged_in`, `logged_out`; restricts the viewer audience
- `target_geolocations` — ISO 3166-2 codes stored via a custom `geolocation_array` attribute type
- `type_of` — enum: `in_house`, `community`, `external`; `community` requires an associated organization
- `expires_at` — optional datetime; cannot be approved if already past

## Scenarios

### Successful creation with minimal required fields

1. Admin navigates to the new billboard page; the controller instantiates an empty `Billboard`.
2. Admin enters body markdown content and selects a valid placement area, leaving all other fields at their defaults.
3. Admin submits the form via POST to `admin_billboards_path`.
4. The controller builds the billboard from permitted params and sets `creator` to the currently signed-in admin.
5. The model renders the body markdown into `processed_html` (before save), then saves.
6. After save, a name is auto-generated as `"Billboard <id>"` if none was provided, and all links in `processed_html` receive a `bb=<id>` query parameter.
7. A success flash is set and the admin is redirected to the edit path for the new billboard.

### Successful creation with full targeting options

1. Admin fills in body markdown, placement area, a hex border color, tag list (up to 25 tags), geolocation targets as ISO 3166-2 codes, display audience, audience segment, browser context, organization ID, type of ad, render mode, and optional expiration date.
2. Admin submits the form.
3. All validations pass: placement area is in the allowed list, color matches the hex format regexp, geolocation codes are enabled, tag count is within limit, and if `community` type then an organization is present.
4. The billboard is saved, `processed_html` is generated, links receive the `bb` param, and if a stale audience segment is associated it is queued for refresh via `AudienceSegmentRefreshWorker`.
5. Admin is redirected to the edit page.

### Validation failure — missing required fields

1. Admin submits the form without a placement area or body markdown.
2. Model validations reject the record: `placement_area` must be present and in `ALLOWED_PLACEMENT_AREAS`; `body_markdown` must be present.
3. The controller catches the failed save, sets a danger flash with the validation errors rendered as a sentence, and re-renders the `new` template.

### Validation failure — community type without organization

1. Admin selects `community` as the ad type but leaves the organization ID blank.
2. The `validates :organization, presence: true, if: :community?` validation fails.
3. The controller re-renders the form with a danger flash listing the error.

### Validation failure — invalid geolocation or expired approval

1. Admin enters geolocation codes that are not in the enabled set (e.g., `"US-UM"`), or sets `approved: true` with an `expires_at` in the past, or selects `home_hero` placement with a non-`in_house` type.
2. The respective custom validators (`validate_geolocations`, `validate_expiration_approval`, `validate_in_house_hero_ads`) add errors to the record.
3. The controller re-renders the form with a danger flash.

## Failures / Exceptions

- Non-admin users receive `Pundit::NotAuthorizedError` when attempting to POST to `admin_billboards_path`.
- More than 25 tags, tags longer than 30 characters, or tags containing non-alphanumeric characters cause a tag validation failure.
- A `home_hero` placement area with any `type_of` other than `in_house` is rejected with an explicit error on `type_of`.
- An `approved: true` billboard whose `expires_at` is already in the past cannot be saved; the admin must either clear the expiration or leave `approved` as false.
- Invalid ISO 3166-2 geolocation codes (including codes for countries not enabled in `Settings::General.billboard_enabled_countries`) produce a per-location error message.
