---
id: "01KHY7Q1GS36R12CK73ZBXPKNQ"
name: "edge_cache_bust_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust.rb
- app/services/edge_cache/bust_article.rb
- app/services/edge_cache/bust_comment.rb
- app/services/edge_cache/bust_organization.rb
- app/services/edge_cache/bust_page.rb
- app/services/edge_cache/bust_podcast.rb
- app/services/edge_cache/bust_podcast_episode.rb
- app/services/edge_cache/bust_tag.rb
- app/services/edge_cache/bust_user.rb
- app/controllers/concerns/edge_cache_safety_check.rb
- app/services/edge_cache/bust/fastly.rb
- app/services/edge_cache/bust/nginx.rb
- app/services/edge_cache/purge_by_key.rb
- spec/services/edge_cache/bust_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::Bust` within the caching domain.

### Behavioral Areas

- **when passing an Array of paths**: Ensures correct behavior under the specified conditions
- **bust_fastly_cache**: Ensures correct behavior under the specified conditions
- **when fastly is not configured**: does not bust a fastly cache
- **when fastly is configured**: does not bust a fastly cache
- **bust_nginx_cache**: Ensures correct behavior under the specified conditions
- **when OpenResty is not configured**: Ensures correct behavior under the specified conditions
- **when OpenResty is configured and available**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/bust.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_article.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_organization.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_page.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_podcast.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_podcast_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_tag.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_user.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/concerns/edge_cache_safety_check.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/edge_cache/bust/fastly.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust/nginx.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: busts each path

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts each path

### S-2: does not bust a fastly cache

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not bust a fastly cache

### S-3: can bust a fastly cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can bust a fastly cache

### S-4: does not bust an nginx cache

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not bust an nginx cache

### S-5: can bust an nginx cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can bust an nginx cache

