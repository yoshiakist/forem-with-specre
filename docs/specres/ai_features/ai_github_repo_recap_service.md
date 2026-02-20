---
id: "01KHY7Q0YG1X09E0BS98K00136"
name: "ai_github_repo_recap_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/github_repo_recap.rb
- app/controllers/ai_chats_controller.rb
- app/controllers/ai_image_generations_controller.rb
- app/policies/ai_image_generation_policy.rb
- app/services/ai/about_page_generator.rb
- app/services/ai/article_check.rb
- app/services/ai/article_enhancer.rb
- app/services/ai/article_quality_assessor.rb
- app/services/ai/badge_criteria_assessor.rb
- app/services/ai/base.rb
- app/services/ai/chat_service.rb
- spec/services/ai/github_repo_recap_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::GithubRepoRecap` within the ai_features domain.

### Behavioral Areas

- **generate**: generates a recap with commits only
- **when there is no activity**: returns nil as there
- **when there are only old pull requests**: returns nil as there
- **when there are only commits (no PRs)**: returns nil as there
- **when there are many commits**: returns nil as there
- **when GitHub API returns an error**: returns a RecapResult with title and body
- **when AI client fails**: calls the AI client with a properly formatted prompt
- **when AI response is malformed**: stops fetching when it encounters PRs before the timeframe

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/github_repo_recap.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/ai_chats_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/ai_image_generations_controller.rb` -- HTTP request routing and response handling
- **Policy layer**: `app/policies/ai_image_generation_policy.rb` -- authorization and access control rules
- **Service layer**: `app/services/ai/about_page_generator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_check.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_enhancer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_quality_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/badge_criteria_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/base.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/chat_service.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns a RecapResult with title and body

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a RecapResult with title and body

### S-2: calls the AI client with a properly formatted prompt

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the AI client with a properly formatted prompt

### S-3: returns nil

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns nil

### S-4: returns nil as there

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns nil as there

### S-5: generates a recap with commits only

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates a recap with commits only

### S-6: includes commit information in the prompt

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes commit information in the prompt

### S-7: limits commits in the prompt to avoid token limits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** limits commits in the prompt to avoid token limits

### S-8: handles errors gracefully and returns nil

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles errors gracefully and returns nil

### S-9: logs the error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the error

### S-10: handles errors gracefully and returns nil

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles errors gracefully and returns nil

### S-11: logs the error with backtrace

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the error with backtrace

### S-12: still extracts what it can and returns a result

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** still extracts what it can and returns a result

