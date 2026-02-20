---
id: "01KHY7Q13FW678WREK162FKQ28"
name: "admin_surveys_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/surveys_controller.rb
- app/javascript/admin/controllers/admin_surveys_controller.js
- app/views/admin/surveys/_form.html.erb (Template)
- app/views/admin/surveys/_poll_fields.html.erb (Template)
- app/views/admin/surveys/edit.html.erb (Template)
- app/views/admin/surveys/index.html.erb (Template)
- app/views/admin/surveys/new.html.erb (Template)
- app/views/admin/surveys/show.html.erb (Template)
- spec/requests/admin/surveys_spec.rb (Test)

## Functional Overview

This specification defines the expected behavior of `"Admin::Surveys"` within the admin domain.

### Behavioral Areas

- **Admin::Surveys**: Ensures correct behavior under the specified conditions
- **GET /admin/content_manager/surveys**: Ensures correct behavior under the specified conditions
- **POST /admin/content_manager/surveys**: Ensures correct behavior under the specified conditions
- **with valid parameters**: Ensures correct behavior under the specified conditions
- **with invalid parameters**: Ensures correct behavior under the specified conditions
- **PATCH /admin/content_manager/surveys/:id**: Ensures correct behavior under the specified conditions
- **DELETE /admin/content_manager/surveys/:id**: can delete a poll via nested attributes


## Scenarios

### S-1: renders the index page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the index page

### S-2: creates a new survey

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new survey

### S-3: creates a scale poll and generates options automatically

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a scale poll and generates options automatically

### S-4: does not create a survey

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a survey

### S-5: updates the survey

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the survey

### S-6: can delete a poll via nested attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can delete a poll via nested attributes

### S-7: deletes the survey

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the survey

