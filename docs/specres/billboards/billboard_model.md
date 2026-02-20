---
id: "01KHY7Q0X7BBVZJPADQ1Y7MYQX"
name: "billboard_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/billboard_placement_area_configs_controller.rb
- app/controllers/admin/billboards_controller.rb
- app/controllers/api/v1/billboards_controller.rb
- app/controllers/billboard_events_controller.rb
- app/controllers/billboards_controller.rb
- app/helpers/billboard_helper.rb
- app/models/billboard.rb
- app/models/billboard_event.rb
- app/models/billboard_placement_area_config.rb
- app/services/billboard_event_rollup.rb
- app/workers/billboard_event_rollup_worker.rb
- app/workers/organizations/track_promotional_billboard_impressions_worker.rb
- spec/models/billboard_spec.rb

## Functional Overview

This specification defines the expected behavior of `Billboard` within the billboards domain.

### Behavioral Areas

- **update_links_with_bb_param**: calls #update_links_with_bb_param after save
- **after_save callback**: refreshes audience segment as an asynchronous callback
- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **expiration validation**: includes billboards with no expiration
- **when range env var is set**: Modifies instead of appending when bb already exists
- **when parsing liquid tags**: Modifies instead of appending when bb already exists
- **when render_mode is set to raw**: Modifies instead of appending when bb already exists

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/billboard_placement_area_configs_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/billboard_events_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/billboards_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/billboard_helper.rb` -- shared view utility methods
- **Model layer**: `app/models/billboard.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/billboard_event.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/billboard_placement_area_config.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/billboard_event_rollup.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/billboard_event_rollup_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/track_promotional_billboard_impressions_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to organization.optional
- have many billboard events.dependent destroy
- validate presence of placement area
- validate presence of body markdown
- have many tags

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: modifies links to include the bb param with the model id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** modifies links to include the bb param with the model id

### S-3: does not modify the processed_html if no links are present

- **Given** no links are present
- **When** the action is triggered
- **Then** does not modify the processed_html

### S-4: Modifies instead of appending when bb already exists

- **Given** the system is in a standard operational state
- **When** bb already exists
- **Then** Modifies instead of appending

### S-5: properly appends the bb param when the URL already contains query params

- **Given** the system is in a standard operational state
- **When** the URL already contains query params
- **Then** properly appends the bb param

### S-6: does not modify non-http/https links

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not modify non-http/https links

### S-7: modifies relative links

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** modifies relative links

### S-8: calls #update_links_with_bb_param after save

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls #update_links_with_bb_param after save

### S-9: allows sidebar_right

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows sidebar_right

### S-10: allows sidebar_left

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows sidebar_left

### S-11: allows home_hero with in_house

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows home_hero with in_house

### S-12: does not allow home_hero with community

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow home_hero with community

### S-13: disallows unacceptable placement_area

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disallows unacceptable placement_area

