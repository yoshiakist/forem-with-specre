---
id: "01KHY7Q0BA24E38VMNKBDBH7SJ"
name: "badge_uploader_uploader"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/uploaders/badge_uploader.rb
- spec/uploaders/badge_uploader_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badge_Uploader` within the badges domain.

### Behavioral Areas

- **formats**: rejects unsupported formats like pdf
- **exif removal**: removes EXIF and GPS data on upload

### Implementation Architecture

The behavior is implemented across the following layers:

- **Uploader**: `app/uploaders/badge_uploader.rb` -- file upload handling and processing


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

### S-5: permits webp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits webp

### S-6: rejects unsupported formats like pdf

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unsupported formats like pdf

### S-7: removes EXIF and GPS data on upload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes EXIF and GPS data on upload

