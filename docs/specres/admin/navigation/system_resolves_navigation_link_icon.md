---
id: "01KJ7HQJX1MWRVG2NTXVKS5693"
name: "system_resolves_navigation_link_icon"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/navigation_link.rb`
- `app/uploaders/navigation_link_image_uploader.rb`
- `spec/models/navigation_link_spec.rb` (Test)
- `spec/uploaders/navigation_link_image_uploader_spec.rb` (Test)

## Functional Overview

When a `NavigationLink` is saved, the system ensures it always has a displayable icon by applying a three-tier resolution strategy. If the link has an uploaded image, that image URL is used for display. If the link has an inline SVG icon string, that is used instead. If neither is provided, a `before_validation` callback automatically sets the icon to the default SVG read from `app/assets/images/link.svg`, which is cached in memory after the first read. The `NavigationLinkImageUploader` enforces file type and size constraints on uploaded images and generates a UUID-based filename for storage.

## Design Intent

The fallback to a default SVG ensures every navigation link renders consistently in the UI without requiring the admin to always supply an icon. Caching the default SVG content avoids repeated filesystem reads across requests. Prioritizing the uploaded image over the inline SVG in `icon_display` allows admins to upgrade from a text-based icon to a richer image asset without needing to clear the old SVG field.

## Key Members

- `icon` — inline SVG string; must match `<svg ...>` opening tag pattern if present
- `image` — CarrierWave-mounted uploader for raster image files (PNG/JPG)
- `NavigationLinkImageUploader::MAX_FILE_SIZE` — 5 MB upper bound enforced by the uploader
- `NavigationLinkImageUploader::EXTENSION_ALLOWLIST` — `png`, `jpg`, `jpeg`, `jpe` only

## Scenarios

### Icon resolved from uploaded image

1. An admin saves a navigation link with a raster image attached and no inline SVG.
2. The uploader stores the file under `uploads/navigation_link_images/` with a UUID-based filename.
3. `icon_display` returns the uploaded image's URL directly.
4. `icon_url` returns an optimized version of that URL at 24×24 pixels with fill crop.

### Icon resolved from inline SVG

1. An admin saves a navigation link with a valid SVG string in the `icon` field and no image attached.
2. The SVG is validated against the `<svg ...>` pattern; invalid strings cause the record to be rejected.
3. `icon_display` returns the raw SVG string.
4. `icon_url` returns `nil` because no image is mounted.

### Default icon applied when neither icon nor image is provided

1. An admin saves a navigation link with both `icon` and `image` left blank.
2. Before validation, the system reads `app/assets/images/link.svg`, strips surrounding whitespace, and assigns it to `icon`.
3. The record passes validation and is persisted with the default SVG stored in the `icon` column.
4. Subsequent reads of `default_icon_svg` return the same cached object without re-reading the file.

### Uploaded image takes priority over inline SVG

1. A navigation link has both an inline SVG in `icon` and a mounted image.
2. `icon_display` checks for the image first and returns the image URL, ignoring the SVG string.

## Failures / Exceptions

- If `icon` is present but does not match the `<svg ...>` regular expression, the record fails validation and is not saved.
- The uploader rejects files larger than 5 MB or with extensions outside `png`, `jpg`, `jpeg`, `jpe`.
- `icon_url` returns `nil` when no image is attached, so callers must guard against a nil URL.
