---
id: "01KJ6FB22VF10D4883F2B226HM"
name: "admin_can_define_badges"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/badges_controller.rb`
- `app/models/badge.rb`
- `app/uploaders/badge_uploader.rb`
- `app/policies/badge_policy.rb`
- `app/views/admin/badges/index.html.erb` (Template)
- `app/views/admin/badges/new.html.erb` (Template)
- `app/views/admin/badges/edit.html.erb` (Template)
- `spec/requests/admin/badges_spec.rb` (Test)
- `spec/models/badge_spec.rb` (Test)
- `spec/uploaders/badge_uploader_spec.rb` (Test)

## Functional Overview

Administrators can create, view, and update badge definitions through a dedicated admin interface. Each badge requires a title (unique), a description, and an image upload in an approved image format (jpg, jpeg, gif, png, or webp). A URL-safe slug is automatically derived from the title before validation. Badges may optionally award credits and carry a bonus weight for ranking purposes, and may be configured to allow multiple awards to the same user. Only users with admin privileges may access the badge management endpoints.

## Key Members

- `title` — Human-readable badge name; must be unique across all badges.
- `slug` — URL-safe identifier auto-generated from the title via CGI escaping and parameterization; used in the badge's public path (`/badge/<slug>`).
- `description` — Text explaining what the badge represents; required.
- `badge_image` — Uploaded image file (jpg, jpeg, gif, png, or webp); EXIF and GPS metadata are stripped on upload.
- `credits_awarded` — Number of credits granted to a user when the badge is awarded.
- `allow_multiple_awards` — Boolean controlling whether the same user can receive the badge more than once.
- `bonus_weight` — Non-negative integer used for ordering or ranking badge significance.

## Scenarios

### Admin lists all badges

1. An admin navigates to the badge index page.
2. The system retrieves all existing badge records and presents them in the admin interface.

### Admin creates a new badge

1. An admin opens the new badge form.
2. The admin fills in the title, description, credits awarded, and uploads an image in an allowed format.
3. The system auto-generates a slug from the title before saving.
4. On successful save, the admin is redirected to the badge index with a success notice.
5. If any required field is missing or invalid, the form is re-rendered with an error message.

### Admin edits an existing badge

1. An admin opens the edit form for a specific badge.
2. The admin updates one or more fields (e.g., title, description, credits awarded, or image).
3. The system regenerates the slug if the title changed.
4. On successful save, the admin is redirected to the badge index with a success notice.
5. If validation fails, the form is re-rendered with an error message.

### Badge image is stored with EXIF data removed

1. When a badge image is uploaded, the system processes the file through the badge uploader.
2. Any embedded EXIF or GPS metadata is stripped from the image before storage.
3. The cleaned image is saved to the configured upload directory.

### System rejects unsupported image formats

1. An admin attempts to upload a file with an unsupported extension (e.g., PDF).
2. The uploader raises an integrity error and the upload is rejected.

## Failures / Exceptions

- Saving fails if `title` is blank or not unique; the form is re-rendered with the error.
- Saving fails if `description` or `badge_image` is blank; the form is re-rendered with the error.
- Saving fails if `bonus_weight` is not a non-negative integer.
- Saving fails if `allow_multiple_awards` is not a boolean value.
- Uploading a non-allowed file type (e.g., PDF) raises `CarrierWave::IntegrityError` and is rejected.
- A badge with existing `badge_achievements` or `tags` cannot be deleted (association restricts destroy with error).
