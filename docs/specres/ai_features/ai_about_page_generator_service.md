---
id: "01KHY7Q0Y6KXN6W5TEM4B7VJW8"
name: "ai_about_page_generator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/about_page_generator.rb
- app/controllers/ai_chats_controller.rb
- app/controllers/ai_image_generations_controller.rb
- app/policies/ai_image_generation_policy.rb
- app/services/ai/article_check.rb
- app/services/ai/article_enhancer.rb
- app/services/ai/article_quality_assessor.rb
- app/services/ai/badge_criteria_assessor.rb
- app/services/ai/base.rb
- app/services/ai/chat_service.rb
- app/services/ai/comment_check.rb
- spec/services/ai/about_page_generator_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::AboutPageGenerator` within the ai_features domain.

### Behavioral Areas

- **generate!**: Ensures correct behavior under the specified conditions
- **when AI call succeeds on first attempt**: retries and eventually succeeds
- **when about page already exists**: creates an about page successfully
- **when AI call fails initially but succeeds on retry**: retries and eventually succeeds
- **when AI call fails all attempts**: logs warning messages for failed attempts
- **when AI response is too short**: accepts shorter content in test environment
- **when AI response is too long**: retries due to content being too long
- **when AI response contains markdown code blocks**: cleans up markdown code blocks

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/about_page_generator.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/ai_chats_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/ai_image_generations_controller.rb` -- HTTP request routing and response handling
- **Policy layer**: `app/policies/ai_image_generation_policy.rb` -- authorization and access control rules
- **Service layer**: `app/services/ai/article_check.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_enhancer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_quality_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/badge_criteria_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/base.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/chat_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/comment_check.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: creates an about page successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an about page successfully

### S-2: logs success message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs success message

### S-3: updates the existing about page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the existing about page

### S-4: logs update message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs update message

### S-5: retries and eventually succeeds

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retries and eventually succeeds

### S-6: logs warning messages for failed attempts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs warning messages for failed attempts

### S-7: logs error and returns without creating page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and returns without creating page

### S-8: retries due to insufficient content

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retries due to insufficient content

### S-9: retries due to content being too long

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retries due to content being too long

### S-10: cleans up markdown code blocks

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cleans up markdown code blocks

### S-11: removes common AI prefixes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes common AI prefixes

### S-12: accepts shorter content in test environment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts shorter content in test environment

