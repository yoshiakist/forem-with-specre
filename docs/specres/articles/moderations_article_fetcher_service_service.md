---
id: "01KHY7PZJP1BZYPX7MFN912GCZ"
name: "moderations_article_fetcher_service_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/moderations/article_fetcher_service.rb
- spec/services/moderations/article_fetcher_service_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderations::ArticleFetcherService` within the articles domain.

### Behavioral Areas

- **call**: Ensures correct behavior under the specified conditions
- **with different parameters**: excludes articles with scores below minimum threshold
- **filtering logic**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/moderations/article_fetcher_service.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns JSON string of articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns JSON string of articles

### S-2: excludes articles with scores below minimum threshold

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes articles with scores below minimum threshold

### S-3: returns different results for different parameters

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns different results for different parameters

### S-4: filters by minimum score threshold

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters by minimum score threshold

### S-5: filters by feed lookback period

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters by feed lookback period

