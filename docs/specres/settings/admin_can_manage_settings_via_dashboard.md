---
id: "01KHZ3R448RA411ZP1V33AX5MR"
name: "admin_can_manage_settings_via_dashboard"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/settings_controller.rb`
- `app/controllers/admin/settings/base_controller.rb`
- `app/controllers/admin/settings/mandatory_settings_controller.rb`
- `app/models/settings/base.rb`
- `app/services/settings/upsert.rb`
- `app/helpers/admin/settings_helper.rb`
- `app/lib/constants/settings.rb`
- `app/assets/stylesheets/settings.scss`
- `app/views/admin/settings/show.html.erb` (Template)
- `app/views/admin/settings/_update_setting_button.html.erb` (Template)
- `spec/models/settings/base_spec.rb` (Test)

## Functional Overview

Super-admins can access a centralized settings dashboard at `/admin/customization/config` to view and update all site-wide configuration. The dashboard renders collapsible sections for each settings category (authentication, campaigns, community, general, rate limits, SMTP, user experience). Each section submits its form to a dedicated sub-controller that inherits from a shared base controller. The base controller delegates persistence to `Settings::Upsert`, which iterates over submitted parameters, coerces types (boolean, array, hash, integer, float, big_decimal, markdown), validates values, and persists them via the `Settings::Base` framework. Settings are cached at both the per-request level (via `RequestStore`) and application level (via `Rails.cache`) with automatic cache invalidation on writes. The framework supports subforem-scoped settings where subforem-specific values override global defaults.

## Design Intent

The settings system uses a three-tier architecture: models define the schema and type system via a DSL, constants provide UI metadata (descriptions, placeholders), and services orchestrate persistence with domain-specific side effects. This separation allows each settings category to have its own controller and model while sharing a single persistence and caching framework.

## Scenarios

### Admin navigates to the settings dashboard

1. Admin with `super_admin` role navigates to `/admin/customization/config`
2. System renders the settings page with collapsible card sections for each category
3. Each section contains form fields with descriptions and placeholders from the corresponding `Constants::Settings` module
4. The update button is only visible to super-admins

### Admin submits a settings form

1. Admin modifies values in a settings section and clicks "Update Settings"
2. The section's sub-controller receives the form parameters
3. `Settings::Upsert` iterates over each parameter, applying type coercion: arrays are compacted and stripped, hashes are converted, strings are stripped, blanks become nil
4. Each value is persisted via the model's setter method (e.g., `Settings::General.set_logo_png`)
5. System returns a JSON response with success or error messages
6. System logs the change to the audit trail

### System validates settings before persistence

1. Each settings model defines validations via the `setting` DSL (e.g., format, inclusion, presence)
2. When an invalid value is submitted, `ActiveRecord::RecordInvalid` is caught
3. The error message is collected and returned to the admin
4. For mandatory settings, each field is validated independently so one failure does not block other fields

### System caches settings with multi-level strategy

1. On first read within a request, system checks `RequestStore` for cached value
2. If not found, system checks `Rails.cache` (1-week expiry)
3. If not found, system queries the database and populates both caches
4. On write, system clears both `RequestStore` and `Rails.cache` entries for the updated setting across all subforems
5. Cache keys incorporate the subforem ID when subforem-scoped settings are in use

### Only super-admins can access settings

1. A non-super-admin user attempts to access `/admin/customization/config`
2. The `authorize_super_admin` before-action checks `current_user.super_admin?`
3. System raises `Pundit::NotAuthorizedError` and denies access
