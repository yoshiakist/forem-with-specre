---
id: "01KHY7Q1JYS00MRRRJ2FE36KTD"
name: "surveys_controller_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/surveys_controller.rb
- app/controllers/surveys_controller.rb
- spec/requests/surveys_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `"SurveysController"` within the surveys domain.

### Behavioral Areas

- **SurveysController**: Ensures correct behavior under the specified conditions
- **GET /survey/:slug**: Ensures correct behavior under the specified conditions
- **GET /surveys/:id/votes**: Ensures correct behavior under the specified conditions
- **when user has not completed the survey**: renders the show page for an active survey
- **when user has completed the survey with resubmission allowed**: renders the show page for an active survey
- **when user has completed the survey with resubmission not allowed**: renders the show page for an active survey

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/surveys_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/surveys_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: renders the show page for an active survey

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the show page for an active survey

### S-2: redirects when using an old slug

- **Given** the system is in a standard operational state
- **When** using an old slug
- **Then** redirects

### S-3: redirects when using an old old slug

- **Given** the system is in a standard operational state
- **When** using an old old slug
- **Then** redirects

### S-4: returns 404 for non-existent survey

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 404 for non-existent survey

### S-5: returns 404 for inactive survey

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 404 for inactive survey

### S-6: returns empty votes and allows submission

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns empty votes and allows submission

### S-7: returns empty votes for new session and allows resubmission

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns empty votes for new session and allows resubmission

### S-8: returns existing votes and prevents resubmission

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns existing votes and prevents resubmission

