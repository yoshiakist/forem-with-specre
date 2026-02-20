---
id: "01KHY7PZGAP087PTM5D8BE6CMJ"
name: "ai_article_quality_assessor_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/article_quality_assessor.rb
- app/services/ai/article_check.rb
- app/services/ai/article_enhancer.rb
- app/services/email_digest_article_collector.rb
- spec/services/ai/article_quality_assessor_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::ArticleQualityAssessor` within the articles domain.

### Behavioral Areas

- **assess**: falls back to score-based assessment
- **when no articles are provided**: uses AI to identify best and worst articles
- **when only one article is provided**: returns the same article for both best and worst
- **when multiple articles are provided**: uses AI to identify best and worst articles
- **when AI responds successfully**: Ensures correct behavior under the specified conditions
- **when AI responds with different indices**: calls the AI with a properly formatted prompt
- **when internal_content_description_spec is available**: Ensures correct behavior under the specified conditions
- **when subforem_id is provided**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/article_quality_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_check.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_enhancer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/email_digest_article_collector.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns nil for both best and worst

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns nil for both best and worst

### S-2: returns the same article for both best and worst

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the same article for both best and worst

### S-3: uses AI to identify best and worst articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses AI to identify best and worst articles

### S-4: calls the AI with a properly formatted prompt

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the AI with a properly formatted prompt

### S-5: correctly maps AI response to articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** correctly maps AI response to articles

### S-6: uses the internal content description in the prompt

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the internal content description in the prompt

### S-7: uses subforem-specific community description

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses subforem-specific community description

### S-8: falls back to score-based assessment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to score-based assessment

### S-9: falls back to score-based assessment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to score-based assessment

### S-10: falls back to score-based assessment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to score-based assessment

### S-11: logs the error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the error

