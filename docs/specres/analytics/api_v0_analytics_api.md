---
id: "01KHY7Q0YYCMHW7S2EBK4PJN1M"
name: "api_v0_analytics_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/analytics_controller.rb
- app/controllers/api/v1/analytics_controller.rb
- app/controllers/concerns/api/analytics_controller.rb
- app/services/analytics_service.rb
- spec/requests/api/v0/analytics_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V0::Analytics"` within the analytics domain.

### Behavioral Areas

- **Api::V0::Analytics**: Ensures correct behavior under the specified conditions
- **GET /api/analytics/totals**: Ensures correct behavior under the specified conditions
- **GET /api/analytics/historical**: Ensures correct behavior under the specified conditions
- **when the start parameter is not included**: Ensures correct behavior under the specified conditions
- **when the start parameter has the incorrect format**: Ensures correct behavior under the specified conditions
- **GET /api/analytics/past_day**: Ensures correct behavior under the specified conditions
- **GET /api/analytics/referrers**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/analytics_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/analytics_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/analytics_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/analytics_service.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: fails with an unprocessable entity HTTP error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fails with an unprocessable entity HTTP error

### S-2: renders the proper error message in JSON

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper error message in JSON

### S-3: fails with an unprocessable entity HTTP error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fails with an unprocessable entity HTTP error

### S-4: renders the proper error message in JSON

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper error message in JSON

