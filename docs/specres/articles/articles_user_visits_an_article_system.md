---
id: "01KHY7PZKV2EXHTT6YKKNEAW4T"
name: "articles_user_visits_an_article_system"
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
- spec/system/articles/user_visits_an_article_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Views` within the articles domain.

### Behavioral Areas

- **Views an article**: stops a user from moderating an article
- **sticky nav sidebar**: Ensures correct behavior under the specified conditions
- **when showing the date**: shows the readable publish date
- **when articles have long markdowns and different published dates**: suggests articles by other users if the author has no other articles
- **when articles belong to a collection**: suggests articles by other users if the author has no other articles
- **with regular articles**: suggests articles by other users if the author has no other articles
- **when a crossposted article is between two regular articles**: stops a user from moderating an article
- **when an article is scheduled**: stops a user from moderating an article

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

### S-1: stops a user from moderating an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stops a user from moderating an article

### S-2: shows an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows an article

### S-3: shows non-negative comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows non-negative comments

### S-4: suggests articles by other users if the author has no other articles

- **Given** the author has no other articles
- **When** the action is triggered
- **Then** suggests articles by other users

### S-5: suggests more articles by the author if there are any

- **Given** there are any
- **When** the action is triggered
- **Then** suggests more articles by the author

### S-6: shows the readable publish date

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the readable publish date

### S-7: embeds the published timestamp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** embeds the published timestamp

### S-8: shows the identical readable publish dates in each page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the identical readable publish dates in each page

### S-9: lists the articles in ascending published_at order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists the articles in ascending published_at order

### S-10: lists the articles in ascending order considering crossposted_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists the articles in ascending order considering crossposted_at

### S-11: shows the article edit link for the author

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the article edit link for the author

### S-12: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

