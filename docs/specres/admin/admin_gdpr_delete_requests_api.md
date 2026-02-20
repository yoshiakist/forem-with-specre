---
id: "01KHY7Q11G3505E84GK2TV6PQ9"
name: "admin_gdpr_delete_requests_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/gdpr_delete_requests_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/member_manager/gdpr_delete_requests"` within the admin domain.

### Behavioral Areas

- **/admin/member_manager/gdpr_delete_requests**: Ensures correct behavior under the specified conditions
- **with gdpr request**: displays the gdpr delete requests
- **without gdpr request**: displays the gdpr delete requests


## Scenarios

### S-1: renders successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders successfully

### S-2: displays the gdpr delete requests

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays the gdpr delete requests

### S-3: displays the number of existing requests

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays the number of existing requests

### S-4: destroys the gdpr delete request on confirmation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys the gdpr delete request on confirmation

### S-5: creates a corresponding audit_log on confirmation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a corresponding audit_log on confirmation

### S-6: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

