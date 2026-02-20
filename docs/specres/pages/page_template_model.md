---
id: "01KHY7Q0VW68XY0Z5YRMRH59PG"
name: "page_template_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/page_templates_controller.rb
- app/models/page_template.rb
- app/models/navigation_link.rb
- spec/models/page_template_spec.rb

## Functional Overview

This specification defines the expected behavior of `PageTemplate` within the pages domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **schema_fields**: Ensures correct behavior under the specified conditions
- **render_with_data**: Ensures correct behavior under the specified conditions
- **validate_data**: Ensures correct behavior under the specified conditions
- **fork**: sets forked_from to the original template
- **ancestors**: Ensures correct behavior under the specified conditions
- **re-rendering pages when template changes**: requires a valid template_type

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/page_templates_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/page_template.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/navigation_link.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: requires a name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** requires a name

### S-2: requires a unique name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** requires a unique name

### S-3: requires a valid template_type

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** requires a valid template_type

### S-4: validates data_schema format

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates data_schema format

### S-5: validates that schema fields have names

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates that schema fields have names

### S-6: validates field types

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates field types

### S-7: returns the fields from data_schema

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the fields from data_schema

### S-8: returns empty array if no fields

- **Given** no fields
- **When** the action is triggered
- **Then** returns empty array

### S-9: replaces placeholders with data values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** replaces placeholders with data values

### S-10: uses body_html if body_markdown is blank

- **Given** body_markdown is blank
- **When** the action is triggered
- **Then** uses body_html

### S-11: returns empty string if no content

- **Given** no content
- **When** the action is triggered
- **Then** returns empty string

### S-12: returns errors for missing required fields

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns errors for missing required fields

