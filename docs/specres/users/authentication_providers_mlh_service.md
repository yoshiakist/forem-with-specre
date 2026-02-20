---
id: "01KHY7PZY3P6J2NH9QT7FGBFPZ"
name: "authentication_providers_mlh_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/authentication/providers/mlh.rb
- app/services/authentication/providers.rb
- app/services/authentication/providers/apple.rb
- app/services/authentication/providers/facebook.rb
- app/services/authentication/providers/forem.rb
- app/services/authentication/providers/github.rb
- app/services/authentication/providers/google_oauth2.rb
- app/services/authentication/providers/provider.rb
- app/services/authentication/providers/twitter.rb
- spec/services/authentication/providers/mlh_spec.rb

## Functional Overview

This specification defines the expected behavior of `Authentication::Providers::Mlh` within the users domain.

### Behavioral Areas

- **.official_name**: Ensures correct behavior under the specified conditions
- **.sign_in_path**: Ensures correct behavior under the specified conditions
- **new_user_data**: Ensures correct behavior under the specified conditions
- **existing_user_data**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/authentication/providers/mlh.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/apple.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/facebook.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/forem.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/github.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/google_oauth2.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/provider.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/twitter.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns MyMLH

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns MyMLH

### S-2: returns the correct sign in path without callback_url param

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct sign in path without callback_url param

### S-3: supports additional parameters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports additional parameters

### S-4: maps the correct data for a new user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** maps the correct data for a new user

### S-5: maps the correct data for an existing user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** maps the correct data for an existing user

