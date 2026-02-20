---
id: "01KHY7PZGD6M7K13AN08KYY0T8"
name: "article_with_video_creation_service_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/article_with_video_creation_service.rb
- app/services/ai/article_check.rb
- app/services/ai/article_enhancer.rb
- app/services/ai/article_quality_assessor.rb
- app/services/article_api_index_service.rb
- app/services/articles/attributes.rb
- app/services/articles/builder.rb
- app/services/articles/creator.rb
- app/services/articles/destroyer.rb
- app/services/articles/enrich_image_attributes.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- spec/services/article_with_video_creation_service_spec.rb

## Functional Overview

This specification defines the expected behavior of `ArticleWithVideoCreationService` within the articles domain.

### Behavioral Areas

- **create!**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/article_with_video_creation_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_check.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_enhancer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/article_quality_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/article_api_index_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/attributes.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/builder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/creator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/destroyer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/enrich_image_attributes.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: creates a correct article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct article

