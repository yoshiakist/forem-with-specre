---
id: "01KHY7Q0MMJ8YJ5MCXF46DXPP3"
name: "profile_fields_remove_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/profile_fields/remove.rb
- app/controllers/admin/profile_fields_controller.rb
- app/services/profile_fields/add.rb
- app/services/profile_fields/import_from_csv.rb
- spec/services/profile_fields/remove_spec.rb

## Functional Overview

This specification defines the expected behavior of `ProfileFields::Remove` within the profiles domain.

### Behavioral Areas

- **when successfully removing a profile field**: removes the profile field and store accessor
- **when profile field removal fails**: removes the profile field and store accessor

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/profile_fields/remove.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/profile_fields/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/profile_fields/import_from_csv.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: removes the profile field and store accessor

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the profile field and store accessor

### S-2: returns the correct response object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct response object

### S-3: does not remove a profile field

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not remove a profile field

### S-4: returns the correct response object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct response object

