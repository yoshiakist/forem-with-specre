---
id: "01KHY7Q163FA1WX9E7JC68V29C"
name: "image_uploads_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/concerns/image_uploads.rb
- app/controllers/image_uploads_controller.rb
- spec/requests/image_uploads_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ImageUploads"` within the media domain.

### Behavioral Areas

- **ImageUploads**: Ensures correct behavior under the specified conditions
- **POST/image_uploads**: Ensures correct behavior under the specified conditions
- **when not logged-in**: Ensures correct behavior under the specified conditions
- **when logged-in**: Ensures correct behavior under the specified conditions
- **when uploading rate limiting works**: supports for uploading a single image not in an array

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/concerns/image_uploads.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/image_uploads_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: responds with 401

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with 401

### S-2: returns json

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns json

### S-3: provides a link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** provides a link

### S-4: supports for uploading a single image not in an array

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports for uploading a single image not in an array

### S-5: supports upload of more than one image at a time

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports upload of more than one image at a time

### S-6: prevents image with resolutions larger than 4096x4096

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents image with resolutions larger than 4096x4096

### S-7: returns a JSON error if something goes wrong

- **Given** something goes wrong
- **When** the action is triggered
- **Then** returns a JSON error

### S-8: returns error if image file name is too long

- **Given** image file name is too long
- **When** the action is triggered
- **Then** returns error

### S-9: returns error if image file is not a file

- **Given** image file is not a file
- **When** the action is triggered
- **Then** returns error

### S-10: counts number of uploads in cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts number of uploads in cache

### S-11: responds with HTTP 429 with too many uploads

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with HTTP 429 with too many uploads

