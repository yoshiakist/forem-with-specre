---
id: "01KHY7Q11ZC3DM1J4TPJF1Z27A"
name: "admin_navigation_link_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/navigation_link_spec.rb

## Functional Overview

This specification defines the expected behavior of `"NavigationLinks"` within the admin domain.

### Behavioral Areas

- **NavigationLinks**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/navigation_link**: Ensures correct behavior under the specified conditions
- **POST /admin/customization/navigation_link**: Ensures correct behavior under the specified conditions
- **PUT /admin/customization/navigation_links/:id**: Ensures correct behavior under the specified conditions
- **DELETE /admin/customization/navigation_links/:id**: deletes release-tied fragment caches


## Scenarios

### S-1: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-2: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-3: deletes release-tied fragment caches

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes release-tied fragment caches

### S-4: creates a navigation link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a navigation link

### S-5: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-6: updates the navigation-link field values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the navigation-link field values

### S-7: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-8: removes a navigation_link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes a navigation_link

