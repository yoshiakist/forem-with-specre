---
id: "01KHY7Q0WCS2J90CFKC5RNDNN4"
name: "page_templates_re_render_pages_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/page_templates/re_render_pages_worker.rb
- app/controllers/admin/page_templates_controller.rb
- spec/workers/page_templates/re_render_pages_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `PageTemplates::ReRenderPagesWorker` within the pages domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/page_templates/re_render_pages_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/page_templates_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: re-renders all pages belonging to the template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** re-renders all pages belonging to the template

### S-2: does nothing if template is not found

- **Given** template is not found
- **When** the action is triggered
- **Then** does nothing

### S-3: continues processing other pages if one fails

- **Given** one fails
- **When** the action is triggered
- **Then** continues processing other pages

