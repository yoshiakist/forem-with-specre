---
id: "01KHY7Q0WA0N2K6QM0QD7X376Z"
name: "navigation_link_image_uploader_uploader"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/uploaders/navigation_link_image_uploader.rb
- spec/uploaders/navigation_link_image_uploader_spec.rb

## Functional Overview

This specification defines the expected behavior of `NavigationLinkImageUploader` within the pages domain.

### Behavioral Areas

- **formats**: rejects unsupported formats like webp
- **filename**: Ensures correct behavior under the specified conditions
- **file size limits**: stores files in the correct directory
- **content type allowlist**: only allows specific image types

### Implementation Architecture

The behavior is implemented across the following layers:

- **Uploader**: `app/uploaders/navigation_link_image_uploader.rb` -- file upload handling and processing


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

### S-5: rejects unsupported formats like webp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unsupported formats like webp

### S-6: rejects unsupported formats like SVG

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unsupported formats like SVG

### S-7: uses a secure token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses a secure token

### S-8: contains the original file extension when a file is stored

- **Given** the system is in a standard operational state
- **When** a file is stored
- **Then** contains the original file extension

### S-9: has a maximum file size of 5MB

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has a maximum file size of 5MB

### S-10: only allows specific image types

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only allows specific image types

