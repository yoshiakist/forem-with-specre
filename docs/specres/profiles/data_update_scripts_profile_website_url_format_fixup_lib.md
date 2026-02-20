---
id: "01KHY7Q0JYJB8S2NTEXBDB4MJW"
name: "data_update_scripts_profile_website_url_format_fixup_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/profile_field_groups_controller.rb
- app/controllers/admin/profile_fields_controller.rb
- app/controllers/api/v0/profile_images_controller.rb
- app/controllers/api/v1/profile_images_controller.rb
- app/controllers/concerns/api/profile_images_controller.rb
- app/controllers/profile_field_groups_controller.rb
- spec/lib/data_update_scripts/profile_website_url_format_fixup_spec.rb

## Functional Overview

This specification defines the expected behavior of `Profile_Website_Url_Format_Fixup` within the profiles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_field_groups_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: does not modify profiles where website url is null

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not modify profiles where website url is null

### S-2: does not modify profiles where website url is empty

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not modify profiles where website url is empty

### S-3: does not modify profiles where website url is valid

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not modify profiles where website url is valid

### S-4: prepends https:// to invalid urls to make a valid url from hostnames

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prepends https:// to invalid urls to make a valid url from hostnames

### S-5: clears websites that don

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** clears websites that don

### S-6: rejects users in the link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects users in the link

### S-7: trims the input to help parsing

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** trims the input to help parsing

### S-8: handles parse errors by clearing the website url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles parse errors by clearing the website url

