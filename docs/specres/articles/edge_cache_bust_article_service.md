---
id: "01KHY7PZJ6HPGEFZBK4YQJ7JCG"
name: "edge_cache_bust_article_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust_article.rb
- spec/services/edge_cache/bust_article_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::BustArticle` within the articles domain.

### Behavioral Areas

- **when an article is part of an organization**: busts the organization slug

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/bust_article.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: defines TIMEFRAMES

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defines TIMEFRAMES

### S-2: adjusts TIMEFRAMES according to the current time

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adjusts TIMEFRAMES according to the current time

### S-3: busts the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache

### S-4: busts the organization slug

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the organization slug

