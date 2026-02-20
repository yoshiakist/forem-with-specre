---
id: "01KHY7Q0HWGEBNM8M821Q19RD3"
name: "api_v1_organizations_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- app/helpers/admin/organizations_helper.rb
- spec/requests/api/v1/organizations_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::Organizations"` within the organizations domain.

### Behavioral Areas

- **Api::V1::Organizations**: Ensures correct behavior under the specified conditions
- **admin-only endpoints**: Ensures correct behavior under the specified conditions
- **when unauthorized and requesting from an admin-only endpoint**: accepts request and schedules the organization for deletion when found
- **POST /api/organizations**: Ensures correct behavior under the specified conditions
- **when user has site admin privileges and params are valid**: rejects requests with a non-admin token
- **when user does not have site-admin-level privileges**: returns a 401 and does not create the organization
- **when params are invalid**: accepts request and updates the organization with valid params
- **PUT /api/organizations/:id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/organizations_helper.rb` -- shared view utility methods


## Scenarios

### S-1: rejects requests without an authorization token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects requests without an authorization token

### S-2: rejects requests with a non-admin token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects requests with a non-admin token

### S-3: rejects delete requests with a regular admin token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects delete requests with a regular admin token

### S-4: accepts request and creates the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts request and creates the organization

### S-5: returns a 401 and does not create the organization

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a 401 and does not create the organization

### S-6: returns a 422 and does not create the organization

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a 422 and does not create the organization

### S-7: accepts request and updates the organization with valid params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts request and updates the organization with valid params

### S-8: returns a 422 and does not update the organization with invalid params

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a 422 and does not update the organization with invalid params

### S-9: accepts request and schedules the organization for deletion when found

- **Given** the system is in a standard operational state
- **When** found
- **Then** accepts request and schedules the organization for deletion

### S-10: errors if no organization is found

- **Given** no organization is found
- **When** the action is triggered
- **Then** errors

### S-11: responds with an error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with an error

### S-12: retrieves all organizations and renders the collection as json

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retrieves all organizations and renders the collection as json

