---
id: "01KHY7PZFZAYH790B2VGB187V3"
name: "stories_tagged_articles_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/stories/tagged_articles_controller.rb
- app/controllers/stories/articles_search_controller.rb
- app/controllers/stories/pinned_articles_controller.rb
- spec/requests/stories/tagged_articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Stories::TaggedArticlesIndex"` within the articles domain.

### Behavioral Areas

- **Stories::TaggedArticlesIndex**: Ensures correct behavior under the specified conditions
- **when :optimize_article_tag_query is #{method}d**: renders page when tag is not supported but has at least one approved article
- **GET /tag/:tag**: Ensures correct behavior under the specified conditions
- **with caching headers**: renders page and sets proper headers
- **when the tag has moderators**: renders page when tag is not supported but has at least one approved article
- **with user signed in**: renders page with top/week etc.
- **without user signed in**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: renders page and sets proper headers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders page and sets proper headers

### S-2: renders page when tag is not supported but has at least one approved article

- **Given** the system is in a standard operational state
- **When** tag is not supported but has at least one approved article
- **Then** renders page

### S-3: returns not found if no published posts and tag not supported

- **Given** no published posts and tag not supported
- **When** the action is triggered
- **Then** returns not found

### S-4: renders not found if there are approved but scheduled posts

- **Given** there are approved but scheduled posts
- **When** the action is triggered
- **Then** renders not found

### S-5: handles non-basic feed strategy

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles non-basic feed strategy

### S-6: renders normal page if no articles but tag is supported

- **Given** no articles but tag is supported
- **When** the action is triggered
- **Then** renders normal page

### S-7: renders page with top/week etc.

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders page with top/week etc.

### S-8: displays articles with score > -20 on top/week

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays articles with score > -20 on top/week

### S-9: renders tag after alias change

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders tag after alias change

### S-10: shows meta keywords if set

- **Given** set
- **When** the action is triggered
- **Then** shows meta keywords

### S-11: does not show meta keywords if not set

- **Given** not set
- **When** the action is triggered
- **Then** does not show meta keywords

### S-12: shows tags and renders properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows tags and renders properly

