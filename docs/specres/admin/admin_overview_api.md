---
id: "01KHY7Q12EDTYTHBXSZKBP2XGR"
name: "admin_overview_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/overview_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin"` within the admin domain.

### Behavioral Areas

- **/admin**: Ensures correct behavior under the specified conditions
- **Notices**: Ensures correct behavior under the specified conditions
- **Last deployed and Latest Commit ID card**: does not show warning if deployed at is recent
- **analytics**: Ensures correct behavior under the specified conditions
- **GET /admin/stats**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- include "Activity Statistics"
- include "Published Posts"
- include "Comments"
- include "Public Reactions"
- include "New Users"

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: does not show warning if deployed at is recent

- **Given** deployed at is recent
- **When** the action is triggered
- **Then** does not show warning

### S-3: shows warning notice if deployed at is over two weeks ago

- **Given** deployed at is over two weeks ago
- **When** the action is triggered
- **Then** shows warning notice

### S-4: shows danger notice if deployed at is over four weeks ago

- **Given** deployed at is over four weeks ago
- **When** the action is triggered
- **Then** shows danger notice

### S-5: shows the correct value if the Last deployed time is available

- **Given** the Last deployed time is available
- **When** the action is triggered
- **Then** shows the correct value

### S-6: returns stats for the past 7 days by default

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns stats for the past 7 days by default

### S-7: returns stats for the past 30 days when specified

- **Given** the system is in a standard operational state
- **When** specified
- **Then** returns stats for the past 30 days

### S-8: returns stats for the past 90 days when specified

- **Given** the system is in a standard operational state
- **When** specified
- **Then** returns stats for the past 90 days

### S-9: defaults to 7 days for invalid period values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to 7 days for invalid period values

