---
id: "01KHY7Q13H25GT1RRJ39XCQHHN"
name: "admin_tags_moderators_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/tags/moderators_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/content_manager/tags/:id/moderator"` within the admin domain.

### Behavioral Areas

- **/admin/content_manager/tags/:id/moderator**: Ensures correct behavior under the specified conditions
- **POST /admin/content_manager/tags/:id/moderator**: Ensures correct behavior under the specified conditions
- **DELETE /admin/content_manager/tags/:id/moderator**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: adds the given user as trusted and as a tag moderator by username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the given user as trusted and as a tag moderator by username

### S-2: updates user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates user

### S-3: redirects to edit with not_found message when there is no such username

- **Given** the system is in a standard operational state
- **When** there is no such username
- **Then** redirects to edit with not_found message

### S-4: displays error message when notification settings are not updated

- **Given** the system is in a standard operational state
- **When** notification settings are not updated
- **Then** displays error message

### S-5: removes the tag moderator role from the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the tag moderator role from the user

### S-6: does not remove the trusted role from the user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not remove the trusted role from the user

