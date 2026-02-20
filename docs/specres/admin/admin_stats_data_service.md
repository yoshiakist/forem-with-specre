---
id: "01KHY7Q14KKHN9B6KCN7V2ZX6B"
name: "admin_stats_data_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/services/admin/stats_data_spec.rb

## Functional Overview

This specification defines the expected behavior of `Admin::StatsData` within the admin domain.

### Behavioral Areas

- **call**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: returns stats for the specified period

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns stats for the specified period

### S-2: returns stats for 30 days

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns stats for 30 days

### S-3: returns stats for 90 days

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns stats for 90 days

### S-4: defaults to 7 days if no period is specified

- **Given** no period is specified
- **When** the action is triggered
- **Then** defaults to 7 days

### S-5: includes data from the start of the period to now

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes data from the start of the period to now

### S-6: counts only public reactions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts only public reactions

