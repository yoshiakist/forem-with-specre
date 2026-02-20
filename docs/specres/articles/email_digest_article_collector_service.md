---
id: "01KHY7PZJ9S4Z8E5PE07H5XF5W"
name: "email_digest_article_collector_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/email_digest_article_collector.rb
- app/services/ai/article_check.rb
- app/services/ai/article_enhancer.rb
- app/services/ai/article_quality_assessor.rb
- app/services/article_api_index_service.rb
- app/services/article_with_video_creation_service.rb
- app/services/articles/attributes.rb
- app/services/articles/builder.rb
- app/services/articles/creator.rb
- app/services/articles/destroyer.rb
- app/services/articles/enrich_image_attributes.rb
- spec/services/email_digest_article_collector_spec.rb

## Functional Overview

This specification defines the expected behavior of `EmailDigestArticleCollector` within the articles domain.

### Behavioral Areas

- **articles_to_send**: Ensures correct behavior under the specified conditions
- **when user is brand new with no-follow**: provides featured 3 articles and articles tagged with their viewed articles from default subforem
- **when the user has no follows, but does have a few pageviews**: does not filter articles by subforem when user has custom onboarding subforem
- **when user follows subforems**: provides articles only from followed subforems
- **when user follows multiple subforems**: provides articles only from followed subforems
- **when user has custom onboarding subforem**: provides top 3 articles from default subforem
- **when it**: does not filter articles by subforem when user has custom onboarding subforem
- **when it**: does not filter articles by subforem when user has custom onboarding subforem

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/email_digest_article_collector.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_check.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_enhancer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_quality_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/article_api_index_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/article_with_video_creation_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/attributes.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/builder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/creator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/destroyer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/enrich_image_attributes.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: provides top 3 articles from default subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** provides top 3 articles from default subforem

### S-2: marks as not ready if there isn

- **Given** there isn
- **When** the action is triggered
- **Then** marks as not ready

### S-3: marks as not ready if there isn

- **Given** there isn
- **When** the action is triggered
- **Then** marks as not ready

### S-4: provides featured 3 articles and articles tagged with their viewed articles from...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** provides featured 3 articles and articles tagged with their viewed articles from default subforem

### S-5: provides articles tagged with career in addition to featured and viewed from def...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** provides articles tagged with career in addition to featured and viewed from default subforem

### S-6: provides articles only from followed subforems

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** provides articles only from followed subforems

### S-7: falls back to default subforem if not enough articles from followed subforems

- **Given** not enough articles from followed subforems
- **When** the action is triggered
- **Then** falls back to default subforem

### S-8: provides articles from all followed subforems

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** provides articles from all followed subforems

### S-9: does not filter articles by subforem when user has custom onboarding subforem

- **Given** the system is in a standard operational state
- **When** user has custom onboarding subforem
- **Then** does not filter articles by subforem

### S-10: still filters by subforem if user also follows subforems

- **Given** user also follows subforems
- **When** the action is triggered
- **Then** still filters by subforem

### S-11: returns no articles when user shouldn

- **Given** the system is in a standard operational state
- **When** user shouldn
- **Then** returns no articles

### S-12: returns articles even when last email was sent recently if force_send is true

- **Given** the system is in a standard operational state
- **When** last email was sent recently if force_send is true
- **Then** returns articles even

