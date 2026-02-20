---
id: "01KHY7Q1BQ39KVZJV3VSVTXKA4"
name: "images_generate_subforem_images_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/images/generate_subforem_images.rb
- spec/services/images/generate_subforem_images_spec.rb

## Functional Overview

This specification defines the expected behavior of `Images::GenerateSubforemImages` within the subforems domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **call**: creates a new instance and calls it
- **when all operations succeed**: does not use the template when background URL is provided
- **when background URL is provided**: creates a new instance with background URL and calls it
- **when logo png generation fails**: resizes the source image correctly for logo and favicon
- **when resized logo generation fails**: resizes the source image correctly for logo and favicon
- **when favicon generation fails**: resizes the source image correctly for logo and favicon
- **when main social image generation fails**: generates and saves all images successfully

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/images/generate_subforem_images.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: creates a new instance and calls it

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new instance and calls it

### S-2: creates a new instance with background URL and calls it

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new instance with background URL and calls it

### S-3: generates and saves all images successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates and saves all images successfully

### S-4: resizes the source image correctly for logo and favicon

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** resizes the source image correctly for logo and favicon

### S-5: resizes the source image correctly for logo png

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** resizes the source image correctly for logo png

### S-6: creates the social image with correct dimensions and positioning

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates the social image with correct dimensions and positioning

### S-7: uses the custom background URL and crops it to exact dimensions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the custom background URL and crops it to exact dimensions

### S-8: does not use the template when background URL is provided

- **Given** the system is in a standard operational state
- **When** background URL is provided
- **Then** does not use the template

### S-9: logs error and continues with other operations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and continues with other operations

### S-10: logs error and continues with other operations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and continues with other operations

### S-11: logs error and continues with other operations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and continues with other operations

### S-12: logs error and continues with other operations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and continues with other operations

