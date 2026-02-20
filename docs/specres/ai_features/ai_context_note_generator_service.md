---
id: "01KHY7Q0YE3AX4RDH8ZCNTEKFN"
name: "ai_context_note_generator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/context_note_generator.rb
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
- spec/services/ai/context_note_generator_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::ContextNoteGenerator` within the ai_features domain.

### Behavioral Areas

- **call**: Ensures correct behavior under the specified conditions
- **when all data is valid**: Ensures correct behavior under the specified conditions
- **when the AI response is invalid**: creates a context note with the AI response
- **when initialization data is missing**: Ensures correct behavior under the specified conditions
- **when an error occurs**: logs the error and does not crash
- **build_prompt**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/context_note_generator.rb` -- business logic orchestration and domain operations
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

### S-1: creates a context note with the AI response

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a context note with the AI response

### S-2: returns the created context note

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the created context note

### S-3: does not create a context note if response is 

- **Given** response is
- **When** the action is triggered
- **Then** does not create a context note

### S-4: does not create a context note if response is blank

- **Given** response is blank
- **When** the action is triggered
- **Then** does not create a context note

### S-5: returns nil if article is not present

- **Given** article is not present
- **When** the action is triggered
- **Then** returns nil

### S-6: returns nil if tag is not present

- **Given** tag is not present
- **When** the action is triggered
- **Then** returns nil

### S-7: returns nil if tag context note instructions are blank

- **Given** tag context note instructions are blank
- **When** the action is triggered
- **Then** returns nil

### S-8: logs the error and does not crash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the error and does not crash

### S-9: constructs a detailed prompt with article and tag info

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** constructs a detailed prompt with article and tag info

### S-10: returns nil if the tag instructions are blank

- **Given** the tag instructions are blank
- **When** the action is triggered
- **Then** returns nil

