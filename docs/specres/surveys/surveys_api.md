---
id: "01KHY7Q1K0S93T9M0PCT9KVBFG"
name: "surveys_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/surveys_controller.rb
- app/controllers/surveys_controller.rb
- spec/requests/surveys_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Surveys"` within the surveys domain.

### Behavioral Areas

- **Surveys**: Ensures correct behavior under the specified conditions
- **GET /surveys/:id/votes**: Ensures correct behavior under the specified conditions
- **when user is not signed in**: returns an empty votes object if the user has not voted on any poll
- **when user is signed in**: returns an empty votes object if the user has not voted on any poll

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/surveys_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/surveys_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns an unauthorized status

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an unauthorized status

### S-2: returns an empty votes object if the user has not voted on any poll

- **Given** the user has not voted on any poll
- **When** the action is triggered
- **Then** returns an empty votes object

### S-3: returns the user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the user

### S-4: does not include votes for polls outside the specified survey

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include votes for polls outside the specified survey

