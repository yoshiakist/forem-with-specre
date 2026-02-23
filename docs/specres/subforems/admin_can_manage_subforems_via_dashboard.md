---
id: "01KJ4279EDX2T7YVR1AK1GV1W7"
name: "admin_can_manage_subforems_via_dashboard"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- app/controllers/admin/subforems_controller.rb
- app/views/admin/subforems/index.html.erb (Template)
- app/views/admin/subforems/show.html.erb (Template)
- app/views/admin/subforems/new.html.erb (Template)
- app/views/admin/subforems/edit.html.erb (Template)
- app/views/admin/subforems/_form.html.erb (Template)
- spec/requests/admin/subforems_spec.rb (Test)

## Functional Overview

Super admins can list, view, create, and edit subforems through the admin dashboard at `/admin/subforems`. The index page displays all subforems ordered by creation date descending. The show page displays subforem details, community bots, and moderators. Creation supports two modes: when domain, name, brain dump, and logo URL are all provided, the system uses `Subforem.create_from_scratch!` to bootstrap the subforem with AI-generated content; otherwise it falls back to a regular save. Editing allows admins to update all fields including domain, name, and community settings, while moderators are limited to the discoverable flag.

## Design Intent

The admin dashboard provides a centralized interface for platform-wide subforem management, separate from the per-subforem moderator edit page (`SubforemsController#edit`). The dual creation path (create_from_scratch vs. regular save) allows admins to quickly bootstrap fully configured communities using AI or to create minimal subforem records when only basic parameters are available.

## Scenarios

### Admin lists all subforems

1. Admin navigates to `/admin/subforems`
2. System displays all subforems ordered by creation date descending
3. Each row shows the subforem domain as an external link, a View button, and an Edit button

### Admin views subforem details

1. Admin clicks View on a subforem from the index page
2. System displays subforem details: domain, community name, description, tagline, member label, discoverable and root status
3. System displays the community bots section with a link to manage bots
4. System displays current moderators with the ability to add or remove them

### Admin creates a subforem with AI bootstrapping

1. Admin navigates to `/admin/subforems/new`
2. Admin fills in domain, community name, brain dump, logo URL, and optionally background image URL and default locale
3. System calls `Subforem.create_from_scratch!` which creates the record and enqueues `Subforems::CreateFromScratchWorker`
4. Admin is redirected to the index page with a success message

### Admin creates a subforem with minimal parameters

1. Admin navigates to `/admin/subforems/new`
2. Admin fills in only domain and discoverable (omitting brain dump or logo URL)
3. System falls back to a regular `Subforem.new` + `save`
4. Admin is redirected to the index page with a success message

### Admin edits a subforem

1. Admin navigates to the edit page for a subforem
2. Admin can update domain, community name, brain dump, logo URL, background image URL, default locale, discoverable flag, and community settings (description, tagline, member label)
3. System persists subforem attributes and updates `Settings::Community` scoped to the subforem
4. Admin is redirected to the index page with a success message

### Moderator edits a subforem with limited fields

1. A subforem moderator navigates to the edit page
2. Moderator can only update the discoverable flag and community settings
3. Admin-only fields (domain, name, brain dump, logo URL, background image URL, default locale) are not rendered in the form
4. System uses `moderator_params` which permits only `discoverable`

## Failures / Exceptions

- If creation fails due to validation errors, the system re-renders the new form with error messages
- If `Subforem.create_from_scratch!` raises a `StandardError`, the system re-renders the new form with the error message
- If update fails due to validation errors, the system re-renders the edit form with error messages
