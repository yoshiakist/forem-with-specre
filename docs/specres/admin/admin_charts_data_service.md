---
id: "01KHY7Q14GF2R424FJJQXE81B6"
name: "admin_charts_data_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/services/admin/charts_data_spec.rb

## Functional Overview

This specification defines the expected behavior of `Admin::ChartsData` within the admin domain.

### Behavioral Areas

- **current period**: returns proper previous period number


## Scenarios

### S-1: returns proper data type

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper data type

### S-2: returns proper entities

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper entities

### S-3: returns proper previous period number

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper previous period number

### S-4: returns proper number of days of chart data array

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper number of days of chart data array

### S-5: returns proper number of items

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper number of items

### S-6: ignores today

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ignores today

### S-7: goes back seven days by default

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** goes back seven days by default

