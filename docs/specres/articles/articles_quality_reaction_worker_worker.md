---
id: "01KHY7PZN7WJ6EXPPGSD3CY4X9"
name: "articles_quality_reaction_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/articles/quality_reaction_worker.rb
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
- spec/workers/articles/quality_reaction_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::QualityReactionWorker` within the articles domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when mascot user doesn**: applies max_score to the worst article when there are at least 12 articles
- **when no articles exist from the past day**: applies max_score to the worst article when there are at least 12 articles
- **when there are fewer than 5 eligible articles**: applies max_score to the worst article when there are at least 12 articles
- **when there are between 5-11 eligible articles**: applies max_score to the worst article when there are at least 12 articles
- **when articles exist from the past day**: applies max_score to the worst article when there are at least 12 articles
- **when articles are older than 1 day**: applies max_score to the worst article when there are at least 12 articles
- **when articles have negative scores**: applies max_score to the worst article when there are at least 12 articles

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/articles/quality_reaction_worker.rb` -- asynchronous job processing
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

### S-1: does nothing

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does nothing

### S-2: does nothing

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does nothing

### S-3: does nothing

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does nothing

### S-4: only issues thumbs up, not thumbs down

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only issues thumbs up, not thumbs down

### S-5: issues thumbs up to the best article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** issues thumbs up to the best article

### S-6: applies max_score to the worst article when there are at least 12 articles

- **Given** the system is in a standard operational state
- **When** there are at least 12 articles
- **Then** applies max_score to the worst article

### S-7: removes conflicting reactions and applies max_score

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes conflicting reactions and applies max_score

### S-8: logs the actions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the actions

### S-9: does not consider articles older than 1 day

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not consider articles older than 1 day

### S-10: does not consider articles with negative scores

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not consider articles with negative scores

### S-11: does not consider articles that already have mascot reactions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not consider articles that already have mascot reactions

### S-12: still processes the available articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** still processes the available articles

