---
id: "01KHZ42W1F9TF90P5F8MH2WYKZ"
name: "admin_can_configure_user_experience"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/settings/user_experiences_controller.rb`
- `app/models/settings/user_experience.rb`
- `app/lib/constants/settings/user_experience.rb`
- `app/views/admin/settings/forms/_user_experience.html.erb` (Template)
- `spec/models/settings/user_experience_spec.rb` (Test)

## Functional Overview

A super-admin can configure the platform-wide user experience defaults including feed algorithm, visual branding, typography, locale, cover image behavior, and content visibility. The `Settings::UserExperience` model defines settings for feed strategy (basic, configured, large_forem_experimental), feed style (basic, rich, compact), brand color, default font, locale, cover image dimensions, content scoring thresholds, and public/private visibility. The primary brand color is validated for hex format and sufficient color contrast against white to ensure accessibility. These settings serve as site-wide defaults that individual users may override through their personal preferences.

## Scenarios

### Admin sets feed strategy and style

1. Admin selects a `feed_strategy` (basic, configured, or large_forem_experimental)
2. Admin selects a `feed_style` (basic, rich, or compact)
3. Admin sets `feed_lookback_days` (default: 10) to control content freshness window
4. Admin adjusts minimum score thresholds: `home_feed_minimum_score`, `index_minimum_score`, `tag_feed_minimum_score`, `award_tag_minimum_score` (default: 100)
5. System persists the values; the feed algorithm uses these parameters to select and rank content

### Admin configures primary brand color

1. Admin enters `primary_brand_color_hex` as a 3 or 6 character hex code with leading `#`
2. System validates the hex format (rejects non-hex characters and invalid lengths)
3. System checks color contrast against white to ensure accessibility compliance
4. If contrast is insufficient (e.g., white or near-white colors), validation fails with an error
5. Admin can optionally set `accent_background_color_hex` for secondary branding

### Admin sets default font and locale

1. Admin selects `default_font` from: sans_serif, serif, or open_dyslexic
2. Admin selects `default_locale` from available options (e.g., en, fr)
3. System persists as site-wide defaults for new users and anonymous visitors

### Admin toggles public visibility

1. Admin toggles the `public` setting (default: true)
2. When set to false, the platform becomes members-only and content is hidden from anonymous visitors
3. Admin can also toggle `display_in_directory` and `show_mobile_app_banner`

### Admin configures cover image settings

1. Admin sets `cover_image_height` (default: 420 pixels)
2. Admin selects `cover_image_fit` (crop or limit)
3. Admin optionally enters `cover_image_aesthetic_instructions` for AI-assisted image generation
4. Cover image settings support subforem-scoped overrides
