---
id: "01KHY7Q0YBESHG3HFQ8YRFYFGV"
name: "ai_community_copy_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/community_copy.rb
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
- spec/services/ai/community_copy_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::CommunityCopy` within the ai_features domain.

### Behavioral Areas

- **write!**: Ensures correct behavior under the specified conditions
- **when all AI calls succeed on first attempt**: retries and eventually succeeds
- **when AI calls fail initially but succeed on retry**: retries and eventually succeeds
- **when AI calls fail all attempts**: logs warning messages for failed attempts
- **when AI response has extra text that needs cleaning**: cleans description responses with extra text
- **when AI response is too short**: cleans description responses with extra text
- **when saving fails**: logs error and returns without saving
- **response cleaning**: cleans description responses with extra text

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/community_copy.rb` -- business logic orchestration and domain operations
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

### S-1: generates and saves all community copy successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates and saves all community copy successfully

### S-2: retries and eventually succeeds

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retries and eventually succeeds

### S-3: logs warning messages for failed attempts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs warning messages for failed attempts

### S-4: logs error and returns without saving

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and returns without saving

### S-5: cleans description responses with extra text

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cleans description responses with extra text

### S-6: cleans tagline responses with extra text

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cleans tagline responses with extra text

### S-7: cleans content description responses with extra text

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cleans content description responses with extra text

### S-8: retries when description is too short

- **Given** the system is in a standard operational state
- **When** description is too short
- **Then** retries

### S-9: retries when tagline is too short

- **Given** the system is in a standard operational state
- **When** tagline is too short
- **Then** retries

### S-10: logs error when saving description fails

- **Given** the system is in a standard operational state
- **When** saving description fails
- **Then** logs error

### S-11: logs error when saving tagline fails

- **Given** the system is in a standard operational state
- **When** saving tagline fails
- **Then** logs error

### S-12: logs error when saving content description fails

- **Given** the system is in a standard operational state
- **When** saving content description fails
- **Then** logs error

