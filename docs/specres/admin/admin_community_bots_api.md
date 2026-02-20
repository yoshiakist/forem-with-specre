---
id: "01KHY7Q10RW4WS82GD410J80NJ"
name: "admin_community_bots_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/community_bots_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin::CommunityBots"` within the admin domain.

### Behavioral Areas

- **Admin::CommunityBots**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/subforems/:subforem_id/community_bots**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/subforems/:subforem_id/community_bots/new**: Ensures correct behavior under the specified conditions
- **POST /admin/customization/subforems/:subforem_id/community_bots**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/subforems/:subforem_id/community_bots/:id**: Ensures correct behavior under the specified conditions
- **DELETE /admin/customization/subforems/:subforem_id/community_bots/:id**: deletes the community bot


## Scenarios

### S-1: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-2: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-3: creates a new community bot

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new community bot

### S-4: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-5: deletes the community bot

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the community bot

