---
id: "01KHY7Q0YVD41R203A8WYF7GK6"
name: "page_view_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/page_views_controller.rb
- app/models/page_view.rb
- app/services/articles/page_view_updater.rb
- app/services/page_view_rollup.rb
- app/workers/articles/update_organic_page_views_worker.rb
- app/workers/articles/update_page_views_worker.rb
- app/workers/page_view_rollup_worker.rb
- app/models/ahoy/event.rb
- app/models/ahoy/visit.rb
- spec/models/page_view_spec.rb

## Functional Overview

This specification defines the expected behavior of `PageView` within the analytics domain.

### Behavioral Areas

- **when callbacks are triggered before create**: is automatically set when a new page view is created
- **domain**: Ensures correct behavior under the specified conditions
- **path**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/page_views_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/page_view.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/page_view_updater.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/page_view_rollup.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/articles/update_organic_page_views_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/articles/update_page_views_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/page_view_rollup_worker.rb` -- asynchronous job processing
- **Model layer**: `app/models/ahoy/event.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/ahoy/visit.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user.optional
- belong to article

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is automatically set when a new page view is created

- **Given** the system is in a standard operational state
- **When** a new page view is created
- **Then** is automatically set

### S-3: is automatically set when a new page view is created

- **Given** the system is in a standard operational state
- **When** a new page view is created
- **Then** is automatically set

