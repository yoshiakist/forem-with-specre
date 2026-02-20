---
id: "01KHY7PZG72BRHW6XWH5NS2WJK"
name: "ai_article_enhancer_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/article_enhancer.rb
- app/services/ai/article_check.rb
- app/services/ai/article_quality_assessor.rb
- app/services/email_digest_article_collector.rb
- spec/services/ai/article_enhancer_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::ArticleEnhancer` within the articles domain.

### Behavioral Areas

- **calculate_clickbait_score**: Ensures correct behavior under the specified conditions
- **when AI responds with a valid score**: returns the correct clickbait score
- **when AI responds with score above 1.0**: returns the correct clickbait score
- **when AI responds with score below 0.0**: returns the correct clickbait score
- **when AI responds with non-numeric value**: returns empty array without calling AI
- **when AI raises an error**: Ensures correct behavior under the specified conditions
- **generate_tags**: Ensures correct behavior under the specified conditions
- **when article has no tags and candidate tags exist**: returns suggested tags from two-pass selection

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/article_enhancer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_check.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_quality_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/email_digest_article_collector.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns the correct clickbait score

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct clickbait score

### S-2: caps the score at 1.0

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caps the score at 1.0

### S-3: floors the score at 0.0

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** floors the score at 0.0

### S-4: returns 0.0 as default

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 0.0 as default

### S-5: returns 0.0 as fallback after retries

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 0.0 as fallback after retries

### S-6: retries once before falling back

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retries once before falling back

### S-7: logs retry attempts and final fallback

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs retry attempts and final fallback

### S-8: returns suggested tags from two-pass selection

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns suggested tags from two-pass selection

### S-9: calls AI twice for two-pass selection

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls AI twice for two-pass selection

### S-10: returns empty array without calling AI

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns empty array without calling AI

### S-11: returns empty array without calling AI

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns empty array without calling AI

### S-12: returns empty array after first pass

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns empty array after first pass

