---
id: "01KHY7PZQWP55MBXR7SKQBZXPV"
name: "edge_cache_bust_comment_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust_comment.rb
- spec/services/edge_cache/bust_comment_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::BustComment` within the comments domain.

### Behavioral Areas

- **when commentable is an article**: bust article comments
- **when commentable is not an article**: bust article comments

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/bust_comment.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: busts the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache

### S-2: busts the cache for a comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache for a comment

### S-3: bust article comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** bust article comments

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

