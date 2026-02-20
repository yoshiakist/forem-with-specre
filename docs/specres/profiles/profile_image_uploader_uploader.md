---
id: "01KHY7Q0MQAC82T2VQFHS9HRZE"
name: "profile_image_uploader_uploader"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/uploaders/profile_image_uploader.rb
- spec/uploaders/profile_image_uploader_spec.rb

## Functional Overview

This specification defines the expected behavior of `Profile_Image_Uploader` within the profiles domain.

### Behavioral Areas

- **filename**: Ensures correct behavior under the specified conditions
- **formats**: rejects unsupported formats like pdf
- **exif removal**: removes EXIF and GPS data on upload

### Implementation Architecture

The behavior is implemented across the following layers:

- **Uploader**: `app/uploaders/profile_image_uploader.rb` -- file upload handling and processing


## Scenarios

### S-1: stores files in the correct directory

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stores files in the correct directory

### S-2: defaults to nil

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to nil

### S-3: contains a secure token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains a secure token

### S-4: contains the original file extension when a file is stored

- **Given** the system is in a standard operational state
- **When** a file is stored
- **Then** contains the original file extension

### S-5: permits a set of extensions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits a set of extensions

### S-6: permits jpegs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits jpegs

### S-7: permits pngs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits pngs

### S-8: permits webps

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** permits webps

### S-9: rejects unsupported formats like pdf

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unsupported formats like pdf

### S-10: removes EXIF and GPS data on upload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes EXIF and GPS data on upload

