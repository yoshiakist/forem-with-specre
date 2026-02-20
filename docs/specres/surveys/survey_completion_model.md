---
id: "01KHY7Q1JRAEJ6S7RXG3XCKVT9"
name: "survey_completion_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/survey_completion.rb
- app/services/survey_completion_service.rb
- app/models/survey.rb
- spec/models/survey_completion_spec.rb

## Functional Overview

This specification defines the expected behavior of `SurveyCompletion` within the surveys domain.

### Behavioral Areas

- **associations**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions
- **.mark_completed!**: Ensures correct behavior under the specified conditions
- **.user_completed_any?**: Ensures correct behavior under the specified conditions
- **.completed_survey_ids_for_user**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/survey_completion.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/survey_completion_service.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/survey.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user
- belong to survey
- validate presence of completed at

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: validates uniqueness of user_id scoped to survey_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates uniqueness of user_id scoped to survey_id

### S-3: creates a new completion record

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new completion record

### S-4: does not create duplicate completion records

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create duplicate completion records

### S-5: sets completed_at to current time

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets completed_at to current time

### S-6: returns true if user has completed any of the specified surveys

- **Given** user has completed any of the specified surveys
- **When** the action is triggered
- **Then** returns true

### S-7: returns false if user has not completed any of the specified surveys

- **Given** user has not completed any of the specified surveys
- **When** the action is triggered
- **Then** returns false

### S-8: returns false if user is blank

- **Given** user is blank
- **When** the action is triggered
- **Then** returns false

### S-9: returns false if survey_ids is blank

- **Given** survey_ids is blank
- **When** the action is triggered
- **Then** returns false

### S-10: returns survey IDs that the user has completed

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns survey IDs that the user has completed

### S-11: returns empty array if user has not completed any surveys

- **Given** user has not completed any surveys
- **When** the action is triggered
- **Then** returns empty array

### S-12: returns empty array if user is blank

- **Given** user is blank
- **When** the action is triggered
- **Then** returns empty array

