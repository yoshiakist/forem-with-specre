---
id: "01KHY7Q0MJ1BB7SHVP457RV0WV"
name: "profile_fields_import_from_csv_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/profile_fields/import_from_csv.rb
- app/controllers/admin/profile_fields_controller.rb
- app/services/profile_fields/add.rb
- app/services/profile_fields/remove.rb
- spec/services/profile_fields/import_from_csv_spec.rb

## Functional Overview

This specification defines the expected behavior of `ProfileFields::ImportFromCsv` within the profiles domain.

### Behavioral Areas

- **when missing attributes**: handles missing descriptions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/profile_fields/import_from_csv.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/profile_fields/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/profile_fields/remove.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: ignores empty lines

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ignores empty lines

### S-2: imports fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** imports fields

### S-3: handles missing descriptions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles missing descriptions

### S-4: handles missing placeholder_texts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles missing placeholder_texts

### S-5: handles commas in correctly quoted fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles commas in correctly quoted fields

