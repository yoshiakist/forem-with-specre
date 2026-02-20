---
id: "01KHY7PZFGFQ9NH2SR5PNAJ6K1"
name: "articles_articles_update_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/articles_controller.rb
- app/controllers/api/v0/articles_controller.rb
- app/controllers/api/v1/articles_controller.rb
- app/controllers/api/v1/recommended_articles_lists_controller.rb
- app/controllers/articles_controller.rb
- app/controllers/concerns/api/articles_controller.rb
- app/controllers/stories/articles_search_controller.rb
- app/controllers/stories/pinned_articles_controller.rb
- app/controllers/stories/tagged_articles_controller.rb
- app/helpers/articles_helper.rb
- spec/requests/articles/articles_update_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ArticlesUpdate"` within the articles domain.

### Behavioral Areas

- **ArticlesUpdate**: Ensures correct behavior under the specified conditions
- **when setting published_at in editor v2**: adds organization ID when user updates
- **when setting published_at in editor v1**: adds organization ID when user updates
- **when changing an author inside an organization**: adds organization ID when user updates

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/articles_helper.rb` -- shared view utility methods


## Scenarios

### S-1: updates ordinary article with proper params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates ordinary article with proper params

### S-2: returns an unprocessable status with invalid params

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an unprocessable status with invalid params

### S-3: updates article with front matter params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates article with front matter params

### S-4: adds organization ID when user updates

- **Given** the system is in a standard operational state
- **When** user updates
- **Then** adds organization ID

### S-5: removes organization ID when user updates

- **Given** the system is in a standard operational state
- **When** user updates
- **Then** removes organization ID

### S-6: does not modify the organization ID when the user neither adds nor removes the o...

- **Given** the system is in a standard operational state
- **When** the user neither adds nor removes the org
- **Then** does not modify the organization ID

### S-7: does not modify the organization ID when updating someone else

- **Given** the system is in a standard operational state
- **When** updating someone else
- **Then** does not modify the organization ID

### S-8: allows an org admin to assign an org article to another user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an org admin to assign an org article to another user

### S-9: allows super_admin to edit an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows super_admin to edit an article

### S-10: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-11: archives

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** archives

### S-12: updates article collection when new series was passed

- **Given** the system is in a standard operational state
- **When** new series was passed
- **Then** updates article collection

