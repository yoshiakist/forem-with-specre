---
id: "01KHY7Q1G10WYQMAH0EDDH2G0P"
name: "metrics_check_data_update_script_statuses_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/metrics/check_data_update_script_statuses.rb
- spec/workers/metrics/check_data_update_script_statuses_spec.rb

## Functional Overview

This specification defines the expected behavior of `Metrics::CheckDataUpdateScriptStatuses` within the data_scripts domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/metrics/check_data_update_script_statuses.rb` -- asynchronous job processing


## Scenarios

### S-1: logs recently failed script

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs recently failed script

