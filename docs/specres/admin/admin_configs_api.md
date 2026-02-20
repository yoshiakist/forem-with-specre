---
id: "01KHY7Q10V0JXJDDDGMJT90JTA"
name: "admin_configs_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/configs_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/customization/config"` within the admin domain.

### Behavioral Areas

- **/admin/customization/config**: Ensures correct behavior under the specified conditions
- **POST /admin/customization/config as a user**: bars the regular user to access
- **POST /admin/customization/config**: Ensures correct behavior under the specified conditions
- **when admin has typical admin permissions but not super admin**: updates settings admin action taken
- **when admin has full permissions including super**: updates settings admin action taken
- **API tokens**: Ensures correct behavior under the specified conditions
- **Authentication**: updates enabled authentication providers
- **Campaigns**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: bars the regular user to access

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** bars the regular user to access

### S-2: does not allow user to update config

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow user to update config

### S-3: updates settings admin action taken

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates settings admin action taken

### S-4: updates the health_check_token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the health_check_token

### S-5: sets video_encoder_key

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets video_encoder_key

### S-6: updates enabled authentication providers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates enabled authentication providers

### S-7: strips empty elements

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** strips empty elements

### S-8: does not update enabled authentication providers if any associated key missing

- **Given** any associated key missing
- **When** the action is triggered
- **Then** does not update enabled authentication providers

### S-9: enables proper domains to allow list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enables proper domains to allow list

### S-10: does not allow improper domain list

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow improper domain list

### S-11: enables display_email_domain_allow_list_publicly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enables display_email_domain_allow_list_publicly

### S-12: enables email authentication

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enables email authentication

