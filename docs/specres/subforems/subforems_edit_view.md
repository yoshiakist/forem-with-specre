---
id: "01KHY7Q1BX0GFW15JB3WF3747T"
name: "subforems_edit_view"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/subforems_controller.rb
- app/controllers/api/v0/subforems_controller.rb
- app/controllers/api/v1/subforems_controller.rb
- app/controllers/concerns/api/subforems_controller.rb
- app/controllers/subforems_controller.rb
- app/workers/subforems/create_from_scratch_worker.rb
- spec/views/subforems/edit_spec.rb

## Functional Overview

This specification defines the expected behavior of `"subforems/edit"` within the subforems domain.

### Behavioral Areas

- **subforems/edit**: Ensures correct behavior under the specified conditions
- **navigation links form**: displays image upload field before SVG icon field in edit form
- **create form**: displays image upload field before SVG icon field in edit form
- **edit form with existing navigation link**: displays image upload field before SVG icon field in edit form
- **edit form with navigation link that has an image**: displays image upload field before SVG icon field
- **route helpers**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/subforems_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/subforems/create_from_scratch_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: displays image upload field before SVG icon field

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays image upload field before SVG icon field

### S-2: hides SVG icon field by default

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** hides SVG icon field by default

### S-3: includes toggle button for SVG icon field

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes toggle button for SVG icon field

### S-4: includes the toggleSvgIconField JavaScript function

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the toggleSvgIconField JavaScript function

### S-5: displays image upload field before SVG icon field in edit form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays image upload field before SVG icon field in edit form

### S-6: hides SVG icon field by default in edit form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** hides SVG icon field by default in edit form

### S-7: includes unique toggle button for each edit form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes unique toggle button for each edit form

### S-8: displays current image preview in edit form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays current image preview in edit form

### S-9: generates correct path for update_navigation_link with path parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates correct path for update_navigation_link with path parameter

