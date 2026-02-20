---
id: "01KHY7Q0VQDMJ1074FJX55CSP7"
name: "navigation_link_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/navigation_links_controller.rb
- app/models/navigation_link.rb
- app/uploaders/navigation_link_image_uploader.rb
- app/models/page_template.rb
- spec/models/navigation_link_spec.rb

## Functional Overview

This specification defines the expected behavior of `NavigationLink` within the pages domain.

### Behavioral Areas

- **.from_subforem**: Ensures correct behavior under the specified conditions
- **when subforem_id is not explicitly passed**: defaults to RequestStore.store[:subforem_id]
- **when subforem_id is explicitly passed**: defaults to RequestStore.store[:subforem_id]
- **when RequestStore.store[:subforem_id] is nil**: defaults to RequestStore.store[:subforem_id]
- **.create_or_update_by_identity**: Ensures correct behavior under the specified conditions
- **when the url already exists**: sets default icon when both icon and image are blank
- **when the url does not exist**: updates the existing NavigationLink
- **validations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/navigation_links_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/navigation_link.rb` -- data persistence, validations, and associations
- **Uploader**: `app/uploaders/navigation_link_image_uploader.rb` -- file upload handling and processing
- **Model layer**: `app/models/page_template.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of name
- validate presence of url

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: defaults to RequestStore.store[:subforem_id]

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to RequestStore.store[:subforem_id]

### S-3: uses the passed subforem_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the passed subforem_id

### S-4: returns records where subforem_id is nil if no argument is passed

- **Given** no argument is passed
- **When** the action is triggered
- **Then** returns records where subforem_id is nil

### S-5: updates the existing NavigationLink

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the existing NavigationLink

### S-6: creates a new NavigationLink

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new NavigationLink

### S-7: is valid without either icon or image (falls back to default)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid without either icon or image (falls back to default)

### S-8: is valid with an icon and no image

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid with an icon and no image

### S-9: is valid with an image and no icon

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid with an image and no icon

### S-10: validates the icon format

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates the icon format

### S-11: does not allow invalid URLs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow invalid URLs

### S-12: does allow relative URLs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does allow relative URLs

### S-13: normalizes local URLs to relative URLs on save

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** normalizes local URLs to relative URLs on save

