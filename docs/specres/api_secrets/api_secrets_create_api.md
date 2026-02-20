---
id: "01KHY7Q1J52G3CCE7ZNE7SAY3Q"
name: "api_secrets_create_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api_secrets_controller.rb
- app/models/api_secret.rb
- app/policies/api_secret_policy.rb
- spec/requests/api_secrets_create_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ApiSecretsCreate"` within the api_secrets domain.

### Behavioral Areas

- **ApiSecretsCreate**: Ensures correct behavior under the specified conditions
- **POST /users/api_secrets**: Ensures correct behavior under the specified conditions
- **when create succeeds**: creates an ApiSecret for the user
- **when create fails**: creates an ApiSecret for the user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api_secrets_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/api_secret.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/api_secret_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: creates an ApiSecret for the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an ApiSecret for the user

### S-2: sets the description

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the description

### S-3: flashes a message containing the token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** flashes a message containing the token

### S-4: does not create the ApiSecret

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create the ApiSecret

### S-5: flashes an error message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** flashes an error message

