---
id: "01KHY7PZCJD5W6FRD7ER1X9TJF"
name: "data_update_scripts_cleanup_articles_with_invalid_feed_source_url_lib"
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
- spec/lib/data_update_scripts/cleanup_articles_with_invalid_feed_source_url_spec.rb

## Functional Overview

This specification defines the expected behavior of `Cleanup_Articles_With_Invalid_Feed_Source_Url` within the articles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/article_approvals_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: sets feed_source_url to canonical_url if the latter is present

- **Given** the latter is present
- **When** the action is triggered
- **Then** sets feed_source_url to canonical_url

### S-2: sets empty string feed source url to nil

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets empty string feed source url to nil

### S-3: sets totally invalid url to nil

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets totally invalid url to nil

### S-4: sets an 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets an 

