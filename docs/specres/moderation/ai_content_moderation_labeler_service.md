---
id: "01KHY7Q0N293J7QDJCGB3V9J5Y"
name: "ai_content_moderation_labeler_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/content_moderation_labeler.rb
- app/services/ai/profile_moderation_labeler.rb
- app/services/spam/domain_detector.rb
- app/workers/spam/block_domain_and_suspend_users_worker.rb
- spec/services/ai/content_moderation_labeler_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::ContentModerationLabeler` within the moderation domain.

### Behavioral Areas

- **label**: returns the correct label
- **when AI responds successfully**: Ensures correct behavior under the specified conditions
- **when AI raises an error**: Ensures correct behavior under the specified conditions
- **when AI succeeds after retries**: falls back to safe default after retries
- **when AI succeeds on first retry**: logs retry attempts

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/content_moderation_labeler.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/profile_moderation_labeler.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/spam/domain_detector.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/spam/block_domain_and_suspend_users_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns the correct label

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct label

### S-2: falls back to safe default after retries

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to safe default after retries

### S-3: retries exactly 2 times before falling back

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retries exactly 2 times before falling back

### S-4: logs retry attempts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs retry attempts

### S-5: returns the correct label after successful retry

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct label after successful retry

### S-6: makes exactly 3 attempts before succeeding

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** makes exactly 3 attempts before succeeding

### S-7: logs retry attempts but not final fallback

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs retry attempts but not final fallback

### S-8: returns the correct label after first retry

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct label after first retry

### S-9: makes exactly 2 attempts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** makes exactly 2 attempts

