---
id: "01KHY7Q1FWEANXYFNKK2KKS779"
name: "data_update_script_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- app/models/data_update_script.rb
- app/workers/metrics/check_data_update_script_statuses.rb
- spec/models/data_update_script_spec.rb

## Functional Overview

This specification defines the expected behavior of `DataUpdateScript` within the data_scripts domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **.scripts_to_run**: Ensures correct behavior under the specified conditions
- **.scripts_to_run?**: Ensures correct behavior under the specified conditions
- **mark_as_finished!**: Ensures correct behavior under the specified conditions
- **mark_as_run!**: Ensures correct behavior under the specified conditions
- **mark_as_failed!**: Ensures correct behavior under the specified conditions
- **file_path**: returns correct loadable file_path

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/data_update_script.rb` -- data persistence, validations, and associations
- **Background worker**: `app/workers/metrics/check_data_update_script_statuses.rb` -- asynchronous job processing


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of file name
- validate presence of status
- validate uniqueness of file name

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: creates new DataUpdateScripts from files

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates new DataUpdateScripts from files

### S-3: returns scripts that need to be run

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns scripts that need to be run

### S-4: does not return script ids that are running

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return script ids that are running

### S-5: orders scripts by name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** orders scripts by name

### S-6: returns true for a new set of files

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true for a new set of files

### S-7: returns true if there is an enqueued script

- **Given** there is an enqueued script
- **When** the action is triggered
- **Then** returns true

### S-8: returns true if there are multiple files on disk

- **Given** there are multiple files on disk
- **When** the action is triggered
- **Then** returns true

### S-9: returns false if there are only working scripts

- **Given** there are only working scripts
- **When** the action is triggered
- **Then** returns false

### S-10: returns false if there are only succeeded scripts

- **Given** there are only succeeded scripts
- **When** the action is triggered
- **Then** returns false

### S-11: returns false if there are only failed scripts

- **Given** there are only failed scripts
- **When** the action is triggered
- **Then** returns false

### S-12: marks data update script as finished

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks data update script as finished

### S-13: marks data update script as working

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks data update script as working

