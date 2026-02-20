---
id: "01KHY7Q1FD44PV84NPSAKDXZS5"
name: "data_update_scripts_remove_mailchimp_sustaining_members_newsletter_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/remove_mailchimp_sustaining_members_newsletter_spec.rb

## Functional Overview

This specification defines the expected behavior of `Remove_Mailchimp_Sustaining_Members_Newsletter` within the data_scripts domain.

### Behavioral Areas

- **when there is a newsletter setting**: does nothing when setting not present

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: does nothing when setting not present

- **Given** the system is in a standard operational state
- **When** setting not present
- **Then** does nothing

### S-2: removes mailchimp_sustaining_members_id setting

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes mailchimp_sustaining_members_id setting

