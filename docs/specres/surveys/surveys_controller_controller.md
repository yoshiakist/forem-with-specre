---
id: "01KHY7Q1JPFSCE7F2XDFV8V7KX"
name: "surveys_controller_controller"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/surveys_controller.rb
- app/controllers/surveys_controller.rb
- spec/controllers/surveys_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `SurveysController` within the surveys domain.

### Behavioral Areas

- **GET #show**: Ensures correct behavior under the specified conditions
- **GET #votes**: Ensures correct behavior under the specified conditions
- **when user is not authenticated**: redirects when finding by old_slug
- **when user is authenticated**: redirects when finding by old_slug
- **when user has not completed the survey**: finds survey by slug
- **when user has completed the survey**: finds survey by slug
- **when resubmission is not allowed**: redirects when finding by old_slug
- **when resubmission is allowed**: redirects when finding by old_slug

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/surveys_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/surveys_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: finds survey by slug

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds survey by slug

### S-2: redirects when finding by old_slug

- **Given** the system is in a standard operational state
- **When** finding by old_slug
- **Then** redirects

### S-3: redirects when finding by old_old_slug

- **Given** the system is in a standard operational state
- **When** finding by old_old_slug
- **Then** redirects

### S-4: returns 404 for inactive survey

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 404 for inactive survey

### S-5: returns 404 for unknown slug

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 404 for unknown slug

### S-6: redirects to sign in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to sign in

### S-7: returns correct response data

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct response data

### S-8: returns correct response data

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct response data

### S-9: returns correct response data with new session

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct response data with new session

### S-10: includes text responses in the votes data

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes text responses in the votes data

