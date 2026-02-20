---
id: "01KHY7PZNAHM0PQJWE6YZ07Y9N"
name: "articles_score_calc_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/articles/score_calc_worker.rb
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
- spec/workers/articles/score_calc_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::ScoreCalcWorker` within the articles domain.

### Behavioral Areas

- **perform_now**: Ensures correct behavior under the specified conditions
- **with article**: updates article scores
- **without article**: updates article scores

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/articles/score_calc_worker.rb` -- asynchronous job processing
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

### S-1: updates article scores

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates article scores

### S-2: does not error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not error

### S-3: does not calculate scores

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not calculate scores

