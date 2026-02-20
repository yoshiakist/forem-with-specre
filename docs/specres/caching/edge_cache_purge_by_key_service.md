---
id: "01KHY7Q1GYQQ73YD9CA0RD8F0G"
name: "edge_cache_purge_by_key_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/purge_by_key.rb
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
- spec/services/edge_cache/purge_by_key_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::PurgeByKey` within the caching domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/purge_by_key.rb` -- business logic orchestration and domain operations
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

### S-1: purges each surrogate key

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** purges each surrogate key

### S-2: does nothing when fastly is not configured

- **Given** the system is in a standard operational state
- **When** fastly is not configured
- **Then** does nothing

### S-3: falls back to path busting when fastly is not configured

- **Given** the system is in a standard operational state
- **When** fastly is not configured
- **Then** falls back to path busting

