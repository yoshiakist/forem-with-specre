---
id: "01KHY7Q0XG620TWA16HCFSZ32Z"
name: "api_v1_billboards_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/billboards_controller.rb
- app/controllers/api/v1/billboards_controller.rb
- app/controllers/billboards_controller.rb
- spec/requests/api/v1/billboards_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::Billboards"` within the billboards domain.

### Behavioral Areas

- **Api::V1::Billboards**: Ensures correct behavior under the specified conditions
- **when user is authorized**: returns unauthorized
- **when authenticated and authorized and get to index**: returns unauthorized
- **when user is authorized**: returns unauthorized
- **GET /api/billboards**: Ensures correct behavior under the specified conditions
- **POST /api/billboards**: Ensures correct behavior under the specified conditions
- **GET /api/billboards/:id**: Ensures correct behavior under the specified conditions
- **PUT /api/billboards/:id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/billboards_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns json response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns json response

### S-2: creates a new billboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new billboard

### S-3: also accepts target geolocations as an array

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** also accepts target geolocations as an array

### S-4: returns a malformed response with invalid display_to

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a malformed response with invalid display_to

### S-5: returns a malformed response with invalid geolocation

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a malformed response with invalid geolocation

### S-6: returns json response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns json response

### S-7: updates an existing billboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates an existing billboard

### S-8: also accepts target geolocations as an array

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** also accepts target geolocations as an array

### S-9: returns a malformed response with invalid geolocation

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a malformed response with invalid geolocation

### S-10: unpublishes the billboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** unpublishes the billboard

### S-11: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-12: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

