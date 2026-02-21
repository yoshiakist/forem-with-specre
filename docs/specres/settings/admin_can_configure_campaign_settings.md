---
id: "01KHZ3VGDB0VF4P07XM2VKJ4SY"
name: "admin_can_configure_campaign_settings"
status: "draft"
---

## Related Files

- `app/controllers/admin/settings/campaigns_controller.rb`
- `app/models/settings/campaign.rb`
- `app/lib/constants/settings/campaign.rb`
- `app/views/admin/settings/forms/_campaign.html.erb` (Template)

## Functional Overview

A super-admin can configure the campaign feature that showcases promoted content on the platform. Campaign settings control the display name, call-to-action text, featured tags, sidebar visibility and image, article approval requirements, hero HTML variant, and article expiry time. The campaigns controller inherits directly from the settings base controller with no custom upsert logic, delegating all persistence to the standard `Settings::Upsert` service.

## Scenarios

### Admin configures campaign display and call-to-action

1. Admin sets the campaign `display_name` and `call_to_action` text
2. Admin optionally sets a `url` for the campaign link
3. System persists the values via `Settings::Upsert`
4. The campaign appears on the platform with the configured name and CTA

### Admin enables campaign sidebar

1. Admin sets `sidebar_enabled` to true
2. Admin provides a `sidebar_image` URL (validated as a proper URL format)
3. System persists the settings and the sidebar becomes visible in the campaign area

### Admin configures featured tags and article approval

1. Admin sets `featured_tags` as a comma-separated list of tag names
2. Admin toggles `articles_require_approval` to control whether campaign articles need manual approval
3. Admin sets `articles_expiry_time` (in days, default: 4) to control how long articles remain featured

### Admin sets hero HTML variant

1. Admin enters a `hero_html_variant_name` to control the campaign hero section rendering
2. System persists the variant name for use by the campaign display logic
