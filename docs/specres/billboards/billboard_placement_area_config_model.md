---
id: "01KHY7Q0X49XEDX1ZYZAEX93S0"
name: "billboard_placement_area_config_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/billboard_placement_area_configs_controller.rb
- app/models/billboard_placement_area_config.rb
- app/models/billboard.rb
- app/models/billboard_event.rb
- spec/models/billboard_placement_area_config_spec.rb

## Functional Overview

This specification defines the expected behavior of `BillboardPlacementAreaConfig` within the billboards domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **.delivery_rate_for**: Ensures correct behavior under the specified conditions
- **.should_fetch_billboard?**: Ensures correct behavior under the specified conditions
- **caching**: Ensures correct behavior under the specified conditions
- **.config_for_placement_area**: Ensures correct behavior under the specified conditions
- **.cache_expiry_seconds_for**: Ensures correct behavior under the specified conditions
- **.selection_weights_for**: Ensures correct behavior under the specified conditions
- **initialize_weights_from_app_config**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/billboard_placement_area_configs_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/billboard_placement_area_config.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/billboard.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/billboard_event.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: validates presence of placement_area

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates presence of placement_area

### S-2: validates uniqueness of placement_area

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates uniqueness of placement_area

### S-3: validates inclusion of placement_area in allowed areas

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates inclusion of placement_area in allowed areas

### S-4: validates presence of signed_in_rate

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates presence of signed_in_rate

### S-5: validates presence of signed_out_rate

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates presence of signed_out_rate

### S-6: validates signed_in_rate is between 0 and 100

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates signed_in_rate is between 0 and 100

### S-7: validates signed_out_rate is between 0 and 100

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates signed_out_rate is between 0 and 100

### S-8: is valid with valid attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid with valid attributes

### S-9: validates cache_expiry_seconds is a non-negative integer

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates cache_expiry_seconds is a non-negative integer

### S-10: validates cache_expiry_seconds is at most 24 hours

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates cache_expiry_seconds is at most 24 hours

### S-11: is valid with cache_expiry_seconds within range

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid with cache_expiry_seconds within range

### S-12: returns the signed_in_rate for signed in users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the signed_in_rate for signed in users

