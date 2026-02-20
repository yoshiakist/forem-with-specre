---
id: "01KHY7PZMBNP8PASGQR0A18G9C"
name: "dashboards_user_sorts_dashboard_articles_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/articles_controller.rb
- app/controllers/api/v0/articles_controller.rb
- app/controllers/api/v1/articles_controller.rb
- app/controllers/api/v1/recommended_articles_lists_controller.rb
- app/controllers/article_approvals_controller.rb
- app/controllers/articles_controller.rb
- spec/system/dashboards/user_sorts_dashboard_articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Sorting` within the articles domain.

### Behavioral Areas

- **Sorting Dashboard Articles**: shows articles sorted by default in created_at DESC

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/article_approvals_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: shows articles sorted by default in created_at DESC

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles sorted by default in created_at DESC

### S-2: shows articles sorted by created_at ASC

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles sorted by created_at ASC

### S-3: shows articles sorted by comments_count DESC

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles sorted by comments_count DESC

### S-4: shows articles sorted by page_views_count ASC

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles sorted by page_views_count ASC

### S-5: shows articles sorted by public_reactions_count ASC

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles sorted by public_reactions_count ASC

### S-6: shows articles sorted by published_at DESC

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles sorted by published_at DESC

