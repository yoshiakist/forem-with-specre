---
id: "01KHY7Q108K37N79YRQ9BM9JC9"
name: "admin_badge_achievements_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/badge_achievements_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/content_manager/badge_achievements"` within the admin domain.

### Behavioral Areas

- **/admin/content_manager/badge_achievements**: Ensures correct behavior under the specified conditions
- **POST /admin/content_manager/badge_achievements/award_badges**: Ensures correct behavior under the specified conditions
- **when the user is a single resource admin**: does not award a badge if the username provided is not lowercase
- **DELETE /admin/content_manager/badge_achievements/:id**: deletes the badge_achievement


## Scenarios

### S-1: awards the badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards the badge

### S-2: awards badges

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards badges

### S-3: awards badges with default a message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards badges with default a message

### S-4: includes default description if passed as true

- **Given** passed as true
- **When** the action is triggered
- **Then** includes default description

### S-5: does not include default description if passed as false

- **Given** passed as false
- **When** the action is triggered
- **Then** does not include default description

### S-6: does not award a badge and raises an error if a badge is not specified

- **Given** a badge is not specified
- **When** the action is triggered
- **Then** does not award a badge and raises an error

### S-7: does not award a badge if the username provided is not lowercase

- **Given** the username provided is not lowercase
- **When** the action is triggered
- **Then** does not award a badge

### S-8: deletes the badge_achievement

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the badge_achievement

