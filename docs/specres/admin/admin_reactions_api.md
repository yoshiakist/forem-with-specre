---
id: "01KHY7Q132GJ614T54N5W899BM"
name: "admin_reactions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/reactions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/reactions"` within the admin domain.

### Behavioral Areas

- **/admin/reactions**: Ensures correct behavior under the specified conditions
- **PUT /admin/reactions as admin**: Ensures correct behavior under the specified conditions
- **PUT /admin/reactions as non-admin**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: updates reaction to be confirmed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates reaction to be confirmed

### S-2: updates reaction to be invalid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates reaction to be invalid

### S-3: does not set a non-valid status

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set a non-valid status

### S-4: returns HTTP Status 200 upon status update

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns HTTP Status 200 upon status update

### S-5: returns HTTP Status 422 upon status update failure

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns HTTP Status 422 upon status update failure

### S-6: returns expected JSON upon status update

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns expected JSON upon status update

### S-7: returns error upon status update failure

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns error upon status update failure

### S-8: updates reaction to be confirmed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates reaction to be confirmed

