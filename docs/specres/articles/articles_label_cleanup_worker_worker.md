---
id: "01KHY7PZN272B42SJ34780F563"
name: "articles_label_cleanup_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/articles/label_cleanup_worker.rb
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
- spec/workers/articles/label_cleanup_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::LabelCleanupWorker` within the articles domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when there are eligible articles**: processes eligible articles and enqueues HandleSpamWorker jobs
- **when there are no eligible articles**: processes eligible articles and enqueues HandleSpamWorker jobs
- **when articles exist but are not eligible**: processes eligible articles and enqueues HandleSpamWorker jobs
- **private methods**: Ensures correct behavior under the specified conditions
- **find_eligible_articles**: Ensures correct behavior under the specified conditions
- **constants**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/articles/label_cleanup_worker.rb` -- asynchronous job processing
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

### S-1: processes eligible articles and enqueues HandleSpamWorker jobs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** processes eligible articles and enqueues HandleSpamWorker jobs

### S-2: logs the number of articles being processed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the number of articles being processed

### S-3: limits to MAX_ARTICLES_PER_RUN when there are more articles

- **Given** the system is in a standard operational state
- **When** there are more articles
- **Then** limits to MAX_ARTICLES_PER_RUN

### S-4: does not enqueue any HandleSpamWorker jobs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue any HandleSpamWorker jobs

### S-5: logs that no eligible articles were found

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs that no eligible articles were found

### S-6: does not process articles that are too recent

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not process articles that are too recent

### S-7: does not process articles with different labels

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not process articles with different labels

### S-8: logs that no eligible articles were found when none exist

- **Given** the system is in a standard operational state
- **When** none exist
- **Then** logs that no eligible articles were found

### S-9: returns only published articles with no_moderation_label in the correct time ran...

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only published articles with no_moderation_label in the correct time range

### S-10: orders results randomly and limits to MAX_ARTICLES_PER_RUN

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** orders results randomly and limits to MAX_ARTICLES_PER_RUN

### S-11: has the correct MAX_ARTICLES_PER_RUN value

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has the correct MAX_ARTICLES_PER_RUN value

