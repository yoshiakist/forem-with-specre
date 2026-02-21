---
id: "01KHZ440DNT2G0A6E8HAKEZ36P"
name: "creator_can_set_up_initial_community"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/creator_settings_controller.rb`
- `app/forms/creator_settings_form.rb`
- `app/views/admin/creator_settings/new.html.erb` (Template)
- `app/views/admin/creator_settings/_form.html.erb` (Template)
- `spec/forms/creator_settings_form_spec.rb` (Test)
- `spec/requests/admin/creator_settings_spec.rb` (Test)

## Functional Overview

A user with the `creator` role can complete the initial community setup wizard to bootstrap their Forem instance. The wizard is accessed at `/admin/creator_settings/new` and collects the essential settings needed to launch: community name, primary brand color, logo, access mode (invite-only or public), and acknowledgment of code of conduct and terms. The `CreatorSettingsForm` is an ActiveModel form object that validates inputs and coordinates saves across multiple settings models (`Settings::Community`, `Settings::UserExperience`, `Settings::Authentication`, `Settings::General`) in a single operation. On success, the creator's `saw_onboarding` flag is set and `Settings::General.admin_action_taken_at` is timestamped.

## Scenarios

### Creator completes the setup wizard

1. Creator with `creator?` role navigates to `/admin/creator_settings/new`
2. System renders the onboarding wizard page with the setup form
3. Creator enters a community name (required) and primary brand color hex (required)
4. Creator optionally uploads a logo image
5. Creator selects access mode: "Everyone" (public) or "Invite Only"
6. Creator checks the Code of Conduct and Terms and Conditions acknowledgment checkboxes
7. Creator submits the form

### System saves initial settings across models

1. `CreatorSettingsForm` validates presence of `community_name` and `primary_brand_color_hex`
2. Form sets `Settings::Community.community_name` with the provided name
3. Form sets `Settings::UserExperience.primary_brand_color_hex` and `Settings::UserExperience.public` based on inputs
4. Form sets `Settings::Authentication.invite_only_mode` based on access mode selection
5. If a logo is provided, it is uploaded and `Settings::General.original_logo` and `resized_logo` are set
6. The creator user's `saw_onboarding` flag is set to true
7. `Settings::General.admin_action_taken_at` is set to the current time
8. Creator is redirected to the root path

### Non-creator is denied access

1. A user without the `creator?` role attempts to access `/admin/creator_settings/new`
2. The `extra_authorization` check raises `Pundit::NotAuthorizedError`
3. User is denied access to the setup wizard

## Failures / Exceptions

- Missing community name or brand color fails form validation and re-renders the form with errors
- Unchecked code of conduct or terms checkboxes fail inclusion validation
