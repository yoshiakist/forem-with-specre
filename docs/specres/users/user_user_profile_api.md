---
id: "01KHY7PZWZQ0CVTB22H4BVER56"
name: "user_user_profile_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/admin/user_queries_controller.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/user_roles_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- spec/requests/user/user_profile_spec.rb

## Functional Overview

This specification defines the expected behavior of `"UserProfiles"` within the users domain.

### Behavioral Areas

- **UserProfiles**: Ensures correct behavior under the specified conditions
- **GET /:username**: Ensures correct behavior under the specified conditions
- **when has articles**: displays articles with good and bad score
- **when has comments**: displays good standing comments
- **when has articles**: displays articles with good and bad score
- **when organization**: renders organization page if org
- **redirect_if_inactive_in_subforem_for_organization**: Ensures correct behavior under the specified conditions
- **when the organization is**: renders organization page if org

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/user_roles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: renders to appropriate page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders to appropriate page

### S-2: renders pins if any

- **Given** any
- **When** the action is triggered
- **Then** renders pins

### S-3: displays only 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays only 

### S-4: calls user by their username in the 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls user by their username in the 

### S-5: does not render pins if they don

- **Given** they don
- **When** the action is triggered
- **Then** does not render pins

### S-6: renders profile page of user after changed username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders profile page of user after changed username

### S-7: renders profile page of user after two changed usernames

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders profile page of user after two changed usernames

### S-8: does not render noindex meta if not suspended

- **Given** not suspended
- **When** the action is triggered
- **Then** does not render noindex meta

### S-9: renders rss feed link if any stories

- **Given** any stories
- **When** the action is triggered
- **Then** renders rss feed link

### S-10: does not render feed link if no stories

- **Given** no stories
- **When** the action is triggered
- **Then** does not render feed link

### S-11: renders sidebar profile field elements in sidebar

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders sidebar profile field elements in sidebar

### S-12: does not render special display header elements naively

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render special display header elements naively

