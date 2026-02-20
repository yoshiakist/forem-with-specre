---
id: "01KHY7Q12GZGGE8F28AG61AZST"
name: "admin_page_templates_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/page_templates_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/customization/page_templates"` within the admin domain.

### Behavioral Areas

- **/admin/customization/page_templates**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/page_templates**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/page_templates/:id**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/page_templates/new**: Ensures correct behavior under the specified conditions
- **POST /admin/customization/page_templates**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/page_templates/:id/edit**: Ensures correct behavior under the specified conditions
- **PATCH /admin/customization/page_templates/:id**: Ensures correct behavior under the specified conditions
- **DELETE /admin/customization/page_templates/:id**: deletes the page template


## Scenarios

### S-1: responds with 200 OK

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with 200 OK

### S-2: displays page templates

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays page templates

### S-3: displays the page template details

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays the page template details

### S-4: shows pages using this template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows pages using this template

### S-5: displays the new template form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays the new template form

### S-6: prefills fields when forking a template

- **Given** the system is in a standard operational state
- **When** forking a template
- **Then** prefills fields

### S-7: creates a new page template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new page template

### S-8: displays errors for invalid input

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays errors for invalid input

### S-9: displays the edit form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays the edit form

### S-10: updates the page template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the page template

### S-11: deletes the page template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the page template

### S-12: prevents deletion when pages exist

- **Given** the system is in a standard operational state
- **When** pages exist
- **Then** prevents deletion

