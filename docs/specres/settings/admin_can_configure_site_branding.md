---
id: "01KHZ3X8Z3Y2RPWBDE48X9GQ3D"
name: "admin_can_configure_site_branding"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/settings/general_settings_controller.rb`
- `app/models/settings/general.rb`
- `app/lib/constants/settings/general.rb`
- `app/services/settings/general/upsert.rb`
- `app/views/admin/settings/forms/_images.html.erb` (Template)
- `app/views/admin/settings/forms/_mascot.html.erb` (Template)
- `app/views/admin/settings/forms/_social_media.html.erb` (Template)
- `app/views/admin/settings/forms/_meta_keywords.html.erb` (Template)
- `spec/models/settings/general_spec.rb` (Test)

## Functional Overview

A super-admin can configure the site's visual identity and public-facing metadata through the general settings section. This includes uploading a primary logo (which is automatically resized with aspect ratio calculation via FastImage), setting the favicon URL, main social image, and mascot image/user. The admin can also set social media handles for multiple platforms and configure meta keywords for SEO. The general settings controller uses `Settings::General::Upsert`, which handles logo upload via `LogoUploader` and cleans tag arrays and credit price inputs before delegation to the standard upsert service. A content cache bust is triggered after successful updates.

## Scenarios

### Admin uploads a site logo

1. Admin uploads a logo image file through the images settings section
2. `Settings::General::Upsert` processes the upload via `LogoUploader`
3. System persists the logo URL in `original_logo` and computes `resized_logo` with aspect ratio calculated by FastImage
4. If FastImage fails to determine dimensions, system falls back gracefully and still persists the logo URL
5. Logo appears across the site header and social share cards

### Admin sets favicon and social image

1. Admin enters URLs for `favicon_url` and `main_social_image`
2. System validates the URLs are properly formatted
3. System persists the values; the favicon appears in browser tabs and the social image is used for Open Graph meta tags

### Admin configures mascot

1. Admin sets `mascot_user_id` (via username-to-ID conversion in the form) and `mascot_image_url`
2. System validates the image URL and persists both values
3. The mascot image and description appear in designated UI areas

### Admin sets social media handles

1. Admin enters handles for supported platforms (Twitter, Facebook, GitHub, LinkedIn, Mastodon, and others) via nested `social_media_handles` fields
2. System persists the hash of handle values
3. `social_media_services` helper provides the handles indexed by service name for use in templates and meta tags

### Admin configures meta keywords

1. Admin enters keywords for multiple contexts (default, article, tag) via nested `meta_keywords` fields
2. System persists the hash of keyword values
3. Keywords appear in the corresponding page `<meta>` tags for SEO
