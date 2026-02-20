---
id: "01KHY7PZGTT4NM29TQGJK5M25Z"
name: "articles_enrich_image_attributes_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/enrich_image_attributes.rb
- app/workers/articles/enrich_image_attributes_worker.rb
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
- spec/services/articles/enrich_image_attributes_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::EnrichImageAttributes` within the articles domain.

### Behavioral Areas

- **when the body has no images**: sets a hardcoded image height for YouTube images
- **when the body has a main image**: sets a hardcoded image height for YouTube images
- **when the body renders a liquid tag with images**: sets a hardcoded image height for YouTube images
- **when the body contains uploaded images**: sets a hardcoded image height for YouTube images
- **when the body contains remote images**: sets a hardcoded image height for YouTube images

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/enrich_image_attributes.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/articles/enrich_image_attributes_worker.rb` -- asynchronous job processing
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

### S-1: does not alter the processed HTML

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not alter the processed HTML

### S-2: sets a hardcoded image height for YouTube images

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets a hardcoded image height for YouTube images

### S-3: sets image height when settings are limit

- **Given** the system is in a standard operational state
- **When** settings are limit
- **Then** sets image height

### S-4: defaults to image height when settings are crop

- **Given** the system is in a standard operational state
- **When** settings are crop
- **Then** defaults to image height

### S-5: falls back to 300 when FastImage times out and cover_image_fit is set to limit

- **Given** the system is in a standard operational state
- **When** FastImage times out and cover_image_fit is set to limit
- **Then** falls back to 300

### S-6: does not alter the processed HTML using CommentTag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not alter the processed HTML using CommentTag

### S-7: does not alter the processed HTML using Github::GitHubIssueTag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not alter the processed HTML using Github::GitHubIssueTag

### S-8: does not alter the processed HTML using Github::GithubReadmeTag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not alter the processed HTML using Github::GithubReadmeTag

### S-9: does not alter the processed HTML using MediumTag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not alter the processed HTML using MediumTag

### S-10: does not alter the processed HTML using LinkTag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not alter the processed HTML using LinkTag

### S-11: does not alter the processed HTML using OrganizationTag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not alter the processed HTML using OrganizationTag

### S-12: does not alter the processed HTML using PodcastTag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not alter the processed HTML using PodcastTag

