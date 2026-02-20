---
id: "01KHY7Q0XACCB2RS5N25BPZGHP"
name: "billboard_survey_exclusion_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/billboard.rb
- app/models/billboard_event.rb
- app/models/billboard_placement_area_config.rb
- spec/models/billboard_survey_exclusion_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Billboard` within the billboards domain.

### Behavioral Areas

- **Billboard Survey Exclusion**: Ensures correct behavior under the specified conditions
- **exclude_user_due_to_survey_completion?**: Ensures correct behavior under the specified conditions
- **when exclude_survey_completions is false**: returns false
- **when user is blank**: filters out blank values
- **when exclude_survey_ids is blank**: filters out blank values
- **when user has completed one of the excluded surveys**: Ensures correct behavior under the specified conditions
- **when user has completed all of the excluded surveys**: Ensures correct behavior under the specified conditions
- **when user has not completed any of the excluded surveys**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/billboard.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/billboard_event.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/billboard_placement_area_config.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-2: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-3: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-4: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

### S-5: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

### S-6: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-7: handles comma-separated string input

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles comma-separated string input

### S-8: handles array input

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles array input

### S-9: filters out blank values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters out blank values

