---
id: "01KHY7Q0Z1BCX8KE82K8G7B8YX"
name: "api_v1_analytics_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/analytics_controller.rb
- app/controllers/api/v1/analytics_controller.rb
- app/controllers/concerns/api/analytics_controller.rb
- app/services/analytics_service.rb
- spec/requests/api/v1/analytics_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::Analytics"` within the analytics domain.

### Behavioral Areas

- **Api::V1::Analytics**: Ensures correct behavior under the specified conditions
- **GET /api/analytics/totals**: Ensures correct behavior under the specified conditions
- **GET /api/analytics/historical**: Ensures correct behavior under the specified conditions
- **when the start parameter is not included**: returns 401 when unauthenticated
- **when the start parameter has the incorrect format**: returns 401 when unauthenticated
- **GET /api/analytics/past_day**: Ensures correct behavior under the specified conditions
- **GET /api/analytics/referrers**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/analytics_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/analytics_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/analytics_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/analytics_service.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns 401 when unauthenticated

- **Given** the system is in a standard operational state
- **When** unauthenticated
- **Then** returns 401

### S-2: fails with an unprocessable entity HTTP error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fails with an unprocessable entity HTTP error

### S-3: renders the proper error message in JSON

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper error message in JSON

### S-4: fails with an unprocessable entity HTTP error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fails with an unprocessable entity HTTP error

### S-5: renders the proper error message in JSON

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper error message in JSON

### S-6: returns 401 when unauthenticated

- **Given** the system is in a standard operational state
- **When** unauthenticated
- **Then** returns 401

### S-7: returns 401 when unauthenticated

- **Given** the system is in a standard operational state
- **When** unauthenticated
- **Then** returns 401

