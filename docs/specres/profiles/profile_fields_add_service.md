---
id: "01KHY7Q0MFENBZZV37F7V2WGPB"
name: "profile_fields_add_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/profile_fields/add.rb
- app/controllers/admin/profile_fields_controller.rb
- app/services/profile_fields/import_from_csv.rb
- app/services/profile_fields/remove.rb
- spec/services/profile_fields/add_spec.rb

## Functional Overview

This specification defines the expected behavior of `ProfileFields::Add` within the profiles domain.

### Behavioral Areas

- **when successfully adding a new profile field**: creates a new profile field and adds a store accessor
- **when profile field creation fails**: creates a new profile field and adds a store accessor

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/profile_fields/add.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/profile_fields/import_from_csv.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/profile_fields/remove.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: creates a new profile field and adds a store accessor

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new profile field and adds a store accessor

### S-2: returns the correct response object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct response object

### S-3: does not create a new profile field or store accessor

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new profile field or store accessor

### S-4: returns the correct response object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct response object

