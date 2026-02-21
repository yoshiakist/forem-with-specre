---
id: "01KHYH43TN4FS8ZYTW757DZBHZ"
name: "moderator_can_update_subforem_settings"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/subforems_controller.rb
- app/views/subforems/edit.html.erb (Template)
- app/javascript/controllers/subforem_image_upload_controller.js
- app/uploaders/subforem_image_uploader.rb
- app/policies/subforem_policy.rb
- spec/requests/subforems_spec.rb (Test)
- spec/views/subforems/edit_spec.rb (Test)
- spec/policies/subforem_policy_spec.rb (Test)

## Functional Overview

Subforem moderators, super moderators, and admins can update a subforem's settings through a comprehensive edit page. The edit page is organized into sections — community settings, feed and content, branding, and image uploads. Access and editable fields are governed by a role-based permission model enforced by `SubforemPolicy`: admins can update all fields (including domain, name, and discoverability), super moderators can update most fields except domain and name, and subforem moderators are limited to community settings, user experience, and image uploads.

## Design Intent

The role-based field restrictions allow delegated management: subforem moderators can customize their community's look and feel without being able to change structural properties like domain or discoverability that affect the broader platform.

## Scenarios

### Moderator updates community settings

1. Moderator navigates to the subforem edit page
2. Moderator updates community description, tagline, or member label
3. System persists the changes via `Settings::Community` scoped to the subforem
4. Moderator is redirected back to the edit page with a success notice

### Moderator updates branding and images

1. Moderator uploads a new main logo, navigation logo, or social card image
2. The `subforem_image_upload_controller` Stimulus controller shows a preview of the selected image
3. `SubforemImageUploader` validates the file type (PNG, JPG, GIF, ICO) and size (up to 8 MB)
4. The uploader generates three versions: `main_logo` (128x128), `nav_logo` (80x80), and `social_card` (1200x630)
5. System updates the subforem's image settings

### Admin updates structural fields

1. Admin navigates to the subforem edit page
2. Admin updates domain, community name, or discoverability toggle
3. System persists the changes to the subforem record
4. Non-admin users cannot see or modify these fields

### Authorization enforces role-based access

1. Super admins and subforem moderators (for their subforem) can access the edit page
2. Regular users receive a forbidden response
3. `SubforemPolicy` gates each operation: `edit?`, `update?`, and nested resource policies delegate to role checks
