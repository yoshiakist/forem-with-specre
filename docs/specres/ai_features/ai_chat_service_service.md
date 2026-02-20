---
id: "01KHY7Q0Y88Q5FGMJ2ZJC07DAM"
name: "ai_chat_service_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/chat_service.rb
- app/controllers/ai_chats_controller.rb
- app/controllers/ai_image_generations_controller.rb
- app/policies/ai_image_generation_policy.rb
- app/services/ai/about_page_generator.rb
- app/services/ai/article_check.rb
- app/services/ai/article_enhancer.rb
- app/services/ai/article_quality_assessor.rb
- app/services/ai/badge_criteria_assessor.rb
- app/services/ai/base.rb
- app/services/ai/comment_check.rb
- spec/services/ai/chat_service_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::ChatService` within the ai_features domain.

### Behavioral Areas

- **generate_response**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/chat_service.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/ai_chats_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/ai_image_generations_controller.rb` -- HTTP request routing and response handling
- **Policy layer**: `app/policies/ai_image_generation_policy.rb` -- authorization and access control rules
- **Service layer**: `app/services/ai/about_page_generator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_check.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_enhancer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_quality_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/badge_criteria_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/base.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/comment_check.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: calls the AI client with a prompt including user context

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the AI client with a prompt including user context

### S-2: maintains history

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** maintains history

