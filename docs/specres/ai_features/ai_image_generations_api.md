---
id: "01KHY7Q0Y362AW1ZRXM8EDA8PM"
name: "ai_image_generations_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/ai_image_generations_controller.rb
- spec/requests/ai_image_generations_spec.rb

## Functional Overview

This specification defines the expected behavior of `"AiImageGenerations"` within the ai_features domain.

### Behavioral Areas

- **AiImageGenerations**: Ensures correct behavior under the specified conditions
- **POST /ai_image_generations**: Ensures correct behavior under the specified conditions
- **when not logged-in**: includes aesthetic instructions when set
- **when logged-in**: includes aesthetic instructions when set
- **when rate limiting works**: generates an image successfully with valid prompt
- **when user is spam**: includes aesthetic instructions when set

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/ai_image_generations_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: responds with 401

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with 401

### S-2: returns json

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns json

### S-3: generates an image successfully with valid prompt

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates an image successfully with valid prompt

### S-4: calculates aspect ratio from subforem settings (crop mode)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calculates aspect ratio from subforem settings (crop mode)

### S-5: calculates aspect ratio from subforem settings (limit mode)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calculates aspect ratio from subforem settings (limit mode)

### S-6: uses 5:4 aspect ratio for taller cover images

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses 5:4 aspect ratio for taller cover images

### S-7: caps height at 500 for aspect ratio calculation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caps height at 500 for aspect ratio calculation

### S-8: includes aesthetic instructions when set

- **Given** the system is in a standard operational state
- **When** set
- **Then** includes aesthetic instructions

### S-9: does not modify prompt when aesthetic instructions are blank

- **Given** the system is in a standard operational state
- **When** aesthetic instructions are blank
- **Then** does not modify prompt

### S-10: falls back to default subforem aesthetic when current subforem value is blank

- **Given** the system is in a standard operational state
- **When** current subforem value is blank
- **Then** falls back to default subforem aesthetic

### S-11: returns error when prompt is blank

- **Given** the system is in a standard operational state
- **When** prompt is blank
- **Then** returns error

### S-12: returns error when prompt is missing

- **Given** the system is in a standard operational state
- **When** prompt is missing
- **Then** returns error

