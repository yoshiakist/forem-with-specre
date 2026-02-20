---
id: "01KHY7Q1J8JT74P41AVQ4ZKVDJ"
name: "api_secrets_destroy_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api_secrets_controller.rb
- app/models/api_secret.rb
- app/policies/api_secret_policy.rb
- spec/requests/api_secrets_destroy_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ApiSecretsDestroy"` within the api_secrets domain.

### Behavioral Areas

- **ApiSecretsDestroy**: Ensures correct behavior under the specified conditions
- **DELETE /users/api_secrets**: deletes the ApiSecret for the user
- **when delete succeeds**: deletes the ApiSecret for the user
- **when delete fails**: deletes the ApiSecret for the user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api_secrets_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/api_secret.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/api_secret_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: deletes the ApiSecret for the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the ApiSecret for the user

### S-2: flashes a notice

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** flashes a notice

### S-3: cannot delete a non existing secret

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cannot delete a non existing secret

### S-4: cannot delete another user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cannot delete another user

### S-5: does not delete the ApiSecret

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not delete the ApiSecret

### S-6: flashes an error message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** flashes an error message

