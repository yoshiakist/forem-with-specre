---
id: "01KHY7Q0W26YGS4Y66H45G99CC"
name: "pages_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/pages_controller.rb
- app/controllers/api/v1/pages_controller.rb
- app/controllers/pages_controller.rb
- app/workers/page_templates/re_render_pages_worker.rb
- spec/requests/pages_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Pages"` within the pages domain.

### Behavioral Areas

- **Pages**: Ensures correct behavior under the specified conditions
- **GET /:slug**: Ensures correct behavior under the specified conditions
- **when redirect_if_different_subforem is triggered**: renders proper text file when template is txt
- **when RequestStore.store[:subforem_id] is set and differs**: does not redirect if RequestStore.store[:subforem_id] is nil
- **when RequestStore.store[:subforem_id] matches the page**: does not redirect if page.subforem_id is nil
- **when RequestStore.store[:subforem_id] or page.subforem_id is nil**: does not redirect if page.subforem_id is nil
- **when json template**: returns json data
- **GET /:slug.txt**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/pages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/pages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/pages_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/page_templates/re_render_pages_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: has proper headline for non-top-level

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has proper headline for non-top-level

### S-2: has proper headline and classes for top-level

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has proper headline and classes for top-level

### S-3: redirects to the subforem-based URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the subforem-based URL

### S-4: does not redirect

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not redirect

### S-5: does not redirect if page.subforem_id is nil

- **Given** page.subforem_id is nil
- **When** the action is triggered
- **Then** does not redirect

### S-6: does not redirect if RequestStore.store[:subforem_id] is nil

- **Given** RequestStore.store[:subforem_id] is nil
- **When** the action is triggered
- **Then** does not redirect

### S-7: returns json data

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns json data

### S-8: returns json data for top level template

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns json data for top level template

### S-9: renders proper text file when template is txt

- **Given** the system is in a standard operational state
- **When** template is txt
- **Then** renders proper text file

### S-10: renders not found when .txt request does not have txt template

- **Given** the system is in a standard operational state
- **When** .txt request does not have txt template
- **Then** renders not found

### S-11: renders proper page when slug has one subdirectory

- **Given** the system is in a standard operational state
- **When** slug has one subdirectory
- **Then** renders proper page

### S-12: renders proper page when slug has two subdirectories

- **Given** the system is in a standard operational state
- **When** slug has two subdirectories
- **Then** renders proper page

