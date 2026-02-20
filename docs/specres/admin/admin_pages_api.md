---
id: "01KHY7Q12KB0ZV4GHHNFFBG7V6"
name: "admin_pages_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/pages_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/customization/pages"` within the admin domain.

### Behavioral Areas

- **/admin/customization/pages**: Ensures correct behavior under the specified conditions
- **when managing feature flags**: allows tech admins to manage the feature flag for a page


## Scenarios

### S-1: allows tech admins to manage the feature flag for a page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows tech admins to manage the feature flag for a page

### S-2: does not allow non tech admins to manage the feature flag for a page

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow non tech admins to manage the feature flag for a page

### S-3: prefills the page when page param is passed to new

- **Given** the system is in a standard operational state
- **When** page param is passed to new
- **Then** prefills the page

