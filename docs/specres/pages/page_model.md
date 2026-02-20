---
id: "01KHY7Q0VTXY5TNRFPZ7QX4S13"
name: "page_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/page_templates_controller.rb
- app/controllers/admin/pages_controller.rb
- app/controllers/api/v1/pages_controller.rb
- app/controllers/pages_controller.rb
- app/models/page_template.rb
- app/workers/page_templates/re_render_pages_worker.rb
- app/models/navigation_link.rb
- spec/models/page_spec.rb

## Functional Overview

This specification defines the expected behavior of `Page` within the pages domain.

### Behavioral Areas

- **.from_subforem**: Ensures correct behavior under the specified conditions
- **when subforem_id is not explicitly passed**: defaults to RequestStore.store[:subforem_id]
- **when subforem_id is explicitly passed**: defaults to RequestStore.store[:subforem_id]
- **when RequestStore.store[:subforem_id] is nil**: defaults to RequestStore.store[:subforem_id]
- **.render_safe_html_for**: Ensures correct behavior under the specified conditions
- **when no matching slug in Page database**: takes organization slug into account
- **when no matching slug and the caller didn**: takes organization slug into account
- **when there**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/page_templates_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/pages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/pages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/pages_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/page_template.rb` -- data persistence, validations, and associations
- **Background worker**: `app/workers/page_templates/re_render_pages_worker.rb` -- asynchronous job processing
- **Model layer**: `app/models/navigation_link.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- be html safe

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

### S-5: raises an exception

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an exception

### S-6: returns the html safe version of the processed_html

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the html safe version of the processed_html

### S-7: requires either body_markdown, body_html, body_json or body_css

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** requires either body_markdown, body_html, body_json or body_css

### S-8: takes organization slug into account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** takes organization slug into account

### S-9: takes podcast slug into account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** takes podcast slug into account

### S-10: takes user username into account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** takes user username into account

### S-11: takes sitemap into account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** takes sitemap into account

### S-12: circumnavigates ReservedWords check

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** circumnavigates ReservedWords check

### S-13: allows / in slug

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows / in slug

