---
id: "01KHY7PZM3RB7REQFHW048GDBV"
name: "articles_user_visits_articles_by_timeframe_system"
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
- spec/system/articles/user_visits_articles_by_timeframe_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the articles domain.

### Behavioral Areas

- **User visits articles by timeframe**: shows correct articles for all tabs for logged out users

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

### S-1: shows correct articles for all tabs for logged out users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows correct articles for all tabs for logged out users

### S-2: /top/week

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /top/week

### S-3: /top/month

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /top/month

### S-4: /top/year

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /top/year

### S-5: /top/infinity

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /top/infinity

### S-6: /latest

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /latest

### S-7: shows correct articles for signed_in user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows correct articles for signed_in user

### S-8: /top/week

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /top/week

### S-9: /top/month

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /top/month

### S-10: /top/year

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /top/year

### S-11: /top/infinity

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /top/infinity

### S-12: /latest

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /latest

