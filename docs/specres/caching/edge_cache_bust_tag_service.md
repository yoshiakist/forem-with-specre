---
id: "01KHY7Q1GWGGGY2QC5ET5YHW40"
name: "edge_cache_bust_tag_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust_tag.rb
- app/controllers/concerns/edge_cache_safety_check.rb
- app/services/edge_cache/bust.rb
- app/services/edge_cache/bust/fastly.rb
- app/services/edge_cache/bust/nginx.rb
- app/services/edge_cache/bust_article.rb
- app/services/edge_cache/bust_comment.rb
- app/services/edge_cache/bust_organization.rb
- app/services/edge_cache/bust_page.rb
- app/services/edge_cache/bust_podcast.rb
- app/services/edge_cache/bust_podcast_episode.rb
- spec/services/edge_cache/bust_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::BustTag` within the caching domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/bust_tag.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/concerns/edge_cache_safety_check.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/edge_cache/bust.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust/fastly.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust/nginx.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_article.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_organization.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_page.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_podcast.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_podcast_episode.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: busts the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache

