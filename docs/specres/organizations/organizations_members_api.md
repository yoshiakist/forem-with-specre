---
id: "01KHY7Q0J2TT8RYY0CEE633N2S"
name: "organizations_members_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/organization_memberships_controller.rb
- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- spec/requests/organizations_members_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Organizations` within the organizations domain.

### Behavioral Areas

- **Organizations Members**: returns only active members (excludes pending)
- **GET /:slug/members**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/organization_memberships_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns only active members (excludes pending)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only active members (excludes pending)

### S-2: returns JSON with only active members

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns JSON with only active members

### S-3: returns 404 for non-existent organization slug

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 404 for non-existent organization slug

### S-4: returns 404 for non-existent organization slug in JSON format

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 404 for non-existent organization slug in JSON format

