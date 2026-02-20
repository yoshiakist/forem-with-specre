---
id: "01KHY7Q0X159YVG8GXWQ06ZQGY"
name: "billboard_event_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/billboard_events_controller.rb
- app/models/billboard_event.rb
- app/services/billboard_event_rollup.rb
- app/workers/billboard_event_rollup_worker.rb
- app/models/billboard.rb
- app/models/billboard_placement_area_config.rb
- spec/models/billboard_event_spec.rb

## Functional Overview

This specification defines the expected behavior of `BillboardEvent` within the billboards domain.

### Behavioral Areas

- **unique_on_user_if_type_of_conversion_category**: Ensures correct behavior under the specified conditions
- **only_recent_registrations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/billboard_events_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/billboard_event.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/billboard_event_rollup.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/billboard_event_rollup_worker.rb` -- asynchronous job processing
- **Model layer**: `app/models/billboard.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/billboard_placement_area_config.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate inclusion of category.in array described class::VALID CATEGORIES
- validate inclusion of context type.in array described class::VALID CONTEXT TYPES

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: adds an error if user has already converted a signup

- **Given** user has already converted a signup
- **When** the action is triggered
- **Then** adds an error

### S-3: adds an error if user has already converted a conversion

- **Given** user has already converted a conversion
- **When** the action is triggered
- **Then** adds an error

### S-4: does not add an error if not a signup or conversion

- **Given** not a signup or conversion
- **When** the action is triggered
- **Then** does not add an error

### S-5: adds an error if user is not a recent registration

- **Given** user is not a recent registration
- **When** the action is triggered
- **Then** adds an error

### S-6: does not add an error if user is a recent registration

- **Given** user is a recent registration
- **When** the action is triggered
- **Then** does not add an error

