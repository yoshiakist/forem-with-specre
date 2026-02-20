---
id: "01KHY7PZMKAWB02VH9WYK1G9XH"
name: "article_image_uploader_uploader"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/uploaders/article_image_uploader.rb
- spec/uploaders/article_image_uploader_spec.rb

## Functional Overview

This specification defines the expected behavior of `Article_Image_Uploader` within the articles domain.

### Behavioral Areas

- **filename**: Ensures correct behavior under the specified conditions
- **formats**: rejects unsupported formats like pdf
- **frame validation**: raises an error if frame count is > FRAME_MAX
- **exif removal**: removes EXIF and GPS data on single frame image upload

### Implementation Architecture

The behavior is implemented across the following layers:

- **Uploader**: `app/uploaders/article_image_uploader.rb` -- file upload handling and processing


## Scenarios

### S-1: stores files in the correct directory

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stores files in the correct directory

### S-2: defaults to nil

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to nil

### S-3: contains the original file extension when a file is stored

- **Given** the system is in a standard operational state
- **When** a file is stored
- **Then** contains the original file extension

### S-4: permits a set of extensions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits a set of extensions

### S-5: permits jpegs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits jpegs

### S-6: permits pngs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits pngs

### S-7: permits webp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits webp

### S-8: rejects unsupported formats like pdf

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unsupported formats like pdf

### S-9: raises an error if frame count is > FRAME_MAX

- **Given** frame count is > FRAME_MAX
- **When** the action is triggered
- **Then** raises an error

### S-10: raises a CarrierWave error which can be parsed if MiniMagick timeout occurs

- **Given** MiniMagick timeout occurs
- **When** the action is triggered
- **Then** raises a CarrierWave error which can be parsed

### S-11: removes EXIF and GPS data on single frame image upload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes EXIF and GPS data on single frame image upload

### S-12: does NOT remove EXIF and GPS data if frame count is > FRAME_STRIP_MAX

- **Given** frame count is > FRAME_STRIP_MAX
- **When** the action is triggered
- **Then** does NOT remove EXIF and GPS data

