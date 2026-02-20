---
id: "01KHY7Q165XANZV53SDZ1ZDWMP"
name: "logo_uploader_uploader"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/uploaders/logo_uploader.rb
- app/uploaders/article_image_uploader.rb
- app/uploaders/badge_uploader.rb
- app/uploaders/base_uploader.rb
- app/uploaders/logo_svg_uploader.rb
- app/uploaders/navigation_link_image_uploader.rb
- app/uploaders/profile_image_uploader.rb
- app/uploaders/subforem_image_uploader.rb
- spec/uploaders/logo_uploader_spec.rb

## Functional Overview

This specification defines the expected behavior of `Logo_Uploader` within the media domain.

### Behavioral Areas

- **formats**: rejects unsupported formats like SVG
- **error handling**: raises a CarrierWave error which can be parsed if MiniMagick timeout occurs
- **exif removal**: removes EXIF and GPS data on single frame image upload
- **resize_image**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Uploader**: `app/uploaders/logo_uploader.rb` -- file upload handling and processing
- **Uploader**: `app/uploaders/article_image_uploader.rb` -- file upload handling and processing
- **Uploader**: `app/uploaders/badge_uploader.rb` -- file upload handling and processing
- **Uploader**: `app/uploaders/base_uploader.rb` -- file upload handling and processing
- **Uploader**: `app/uploaders/logo_svg_uploader.rb` -- file upload handling and processing
- **Uploader**: `app/uploaders/navigation_link_image_uploader.rb` -- file upload handling and processing
- **Uploader**: `app/uploaders/profile_image_uploader.rb` -- file upload handling and processing
- **Uploader**: `app/uploaders/subforem_image_uploader.rb` -- file upload handling and processing


## Scenarios

### S-1: stores files in the correct directory

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stores files in the correct directory

### S-2: permits a set of extensions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits a set of extensions

### S-3: permits jpegs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits jpegs

### S-4: permits pngs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits pngs

### S-5: rejects unsupported formats like SVG

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unsupported formats like SVG

### S-6: rejects unsupported formats like webp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unsupported formats like webp

### S-7: rejects unsupported formats like gifs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unsupported formats like gifs

### S-8: raises a CarrierWave error which can be parsed if MiniMagick timeout occurs

- **Given** MiniMagick timeout occurs
- **When** the action is triggered
- **Then** raises a CarrierWave error which can be parsed

### S-9: removes EXIF and GPS data on single frame image upload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes EXIF and GPS data on single frame image upload

### S-10: creates versions of the image with different filenames

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates versions of the image with different filenames

### S-11: contains the original file extension when a file is stored

- **Given** the system is in a standard operational state
- **When** a file is stored
- **Then** contains the original file extension

### S-12: creates versions of the image with different sizes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates versions of the image with different sizes

