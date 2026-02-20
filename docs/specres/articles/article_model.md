---
id: "01KHY7PZD9B9VN5A0QGNNE113P"
name: "article_model"
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
- app/controllers/concerns/api/articles_controller.rb
- app/controllers/stories/articles_search_controller.rb
- app/controllers/stories/pinned_articles_controller.rb
- app/controllers/stories/tagged_articles_controller.rb
- app/decorators/article_decorator.rb
- app/helpers/articles_helper.rb
- app/models/article.rb
- app/models/concerns/algolia_searchable/searchable_article.rb
- app/models/pinned_article.rb
- spec/models/article_spec.rb

## Functional Overview

This specification defines the expected behavior of `Article` within the articles domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **validate_collection_permission**: Ensures correct behavior under the specified conditions
- **with organization collections**: prevents org member from adding article to org collection with different org_id
- **validate_video**: Ensures correct behavior under the specified conditions
- **when user is new (less than 2 weeks old)**: prevents user from adding article to another user
- **when user is old (more than 2 weeks old)**: prevents user from adding article to another user
- **all_series**: Ensures correct behavior under the specified conditions
- **::admin_published_with**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/article_approvals_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/article_decorator.rb` -- presentation logic and view-model enrichment
- **View helper**: `app/helpers/articles_helper.rb` -- shared view utility methods


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to collection.optional
- belong to organization.optional
- belong to user
- have one discussion lock.dependent delete
- have many comments.dependent nullify
- have many context notifications.dependent delete all
- have many feed events.dependent delete all
- have many mentions.dependent delete all
- have many notification subscriptions.dependent delete all
- have many notifications.dependent delete all
- have many page views.dependent delete all
- have many polls.dependent destroy
- have many profile pins.dependent delete all
- have many rating votes.dependent destroy
- have many sourced subscribers

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: allows article owner to add to their own collection

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows article owner to add to their own collection

### S-3: prevents user from adding article to another user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents user from adding article to another user

### S-4: allows org member to add article to org collection when publishing under org

- **Given** the system is in a standard operational state
- **When** publishing under org
- **Then** allows org member to add article to org collection

### S-5: prevents org member from adding article to org collection when not publishing un...

- **Given** the system is in a standard operational state
- **When** not publishing under org
- **Then** prevents org member from adding article to org collection

### S-6: prevents non-org member from adding article to org collection

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents non-org member from adding article to org collection

### S-7: allows org admin to add article to org collection

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows org admin to add article to org collection

### S-8: prevents org member from adding article to org collection with different org_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents org member from adding article to org collection with different org_id

### S-9: prevents org member from adding article to org collection when org_id doesn

- **Given** the system is in a standard operational state
- **When** org_id doesn
- **Then** prevents org member from adding article to org collection

### S-10: does not allow direct uploads (video present but no allowed source url)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow direct uploads (video present but no allowed source url)

### S-11: allows YouTube videos

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows YouTube videos

### S-12: allows Mux videos

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows Mux videos

### S-13: allows Twitch videos

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows Twitch videos

