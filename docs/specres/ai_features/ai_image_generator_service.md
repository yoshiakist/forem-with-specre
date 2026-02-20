---
id: "01KHY7Q0YKFJ4SWJK5AZ9M9C3N"
name: "ai_image_generator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/image_generator.rb
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
- spec/services/ai/image_generator_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::ImageGenerator` within the ai_features domain.

### Behavioral Areas

- **initialize**: initializes with a prompt
- **generate**: generates and returns an image URL
- **when generation succeeds**: logs the generation process
- **when API returns only image without text**: accepts optional input images
- **when API call fails**: still cleans up temporary files even when upload fails
- **when API returns malformed response**: accepts custom response modalities
- **when image upload fails**: accepts optional input images
- **when API returns no image data**: accepts optional input images

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/image_generator.rb` -- business logic orchestration and domain operations
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

### S-1: initializes with a prompt

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes with a prompt

### S-2: raises error with blank prompt

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises error with blank prompt

### S-3: accepts optional input images

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts optional input images

### S-4: accepts optional aspect ratio

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts optional aspect ratio

### S-5: raises error with invalid aspect ratio

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises error with invalid aspect ratio

### S-6: accepts valid aspect ratios

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid aspect ratios

### S-7: accepts custom response modalities

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts custom response modalities

### S-8: generates and returns an image URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates and returns an image URL

### S-9: logs the generation process

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the generation process

### S-10: uploads the image using ArticleImageUploader

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uploads the image using ArticleImageUploader

### S-11: returns result with nil text_response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns result with nil text_response

### S-12: returns nil

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns nil

