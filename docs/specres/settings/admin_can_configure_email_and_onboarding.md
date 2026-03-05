---
id: "01KHZ3YFTYGEV9977C99CJFBCA"
name: "admin_can_configure_email_and_onboarding"
status: "draft"
---

## Related Files

- `app/controllers/admin/settings/general_settings_controller.rb`
- `app/models/settings/general.rb`
- `app/lib/constants/settings/general.rb`
- `app/services/settings/general/upsert.rb`
- `app/views/admin/settings/forms/_emails.html.erb` (Template)
- `app/views/admin/settings/forms/_newsletter.html.erb` (Template)
- `app/views/admin/settings/forms/_onboarding.html.erb` (Template)
- `app/views/admin/settings/forms/_tags.html.erb` (Template)
- `spec/lib/data_update_scripts/populate_suggested_tags_from_settings_spec.rb` (Test)

## Functional Overview

A super-admin can configure email delivery preferences, Mailchimp newsletter integration, and the onboarding experience for new users. Email settings include the contact email address, a custom email footer (HTML with inline styles), and the periodic digest frequency. Newsletter integration connects to Mailchimp via API key and list IDs for the main newsletter, tag moderator newsletter, and community moderator newsletter. Onboarding settings control the suggested tags shown to new users, the newsletter opt-in step content (heading, header, subheader as markdown), and geolocation-based default email opt-in. The `Settings::General::Upsert` service handles tag creation when suggested or sidebar tags are updated — it calls `Tag.find_or_create_all_with_like_by_name` and toggles the `suggested` flag on the appropriate tags.

## Scenarios

### Admin configures email delivery preferences

1. Admin sets `contact_email` for the platform's public contact address
2. Admin enters `custom_email_footer` HTML content (must use inline styles for email client compatibility)
3. Admin sets `periodic_email_digest` frequency in days
4. System persists the values; the digest frequency controls how often the `EmailDigest` worker sends summary emails

### Admin integrates Mailchimp newsletter

1. Admin enters the `mailchimp_api_key` for API access
2. Admin sets list IDs for `mailchimp_newsletter_id`, `mailchimp_tag_moderators_id`, and `mailchimp_community_moderators_id`
3. System persists the configuration; when `custom_newsletter_configured?` returns true (all three onboarding newsletter settings present), custom newsletter flows are activated

### Admin configures onboarding content

1. Admin enters `suggested_tags` as a comma-separated list of tag names
2. `Settings::General::Upsert` downcases and despacifies the tags, then calls `Tag.find_or_create_all_with_like_by_name` to ensure each tag exists
3. System clears the `suggested` flag on previously suggested tags and sets it on the new list
4. Admin can also set `onboarding_newsletter_content`, heading, and subheading (stored as markdown with auto-processed HTML)

### Admin manages sidebar tags

1. Admin enters `sidebar_tags` as a comma-separated list (validated for lowercase alphanumeric format)
2. System ensures each tag exists via `Tag.find_or_create_all_with_like_by_name`
3. Sidebar tags appear in the homepage sidebar for content discovery

### Admin configures geolocation-based email opt-in

1. Admin sets `geos_with_allowed_default_email_opt_in` (visible only when geolocation feature flag is enabled)
2. System persists the geographic regions where email opt-in is pre-checked during onboarding
